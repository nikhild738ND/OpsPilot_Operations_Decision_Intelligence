import argparse
import gzip
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from google.cloud import bigquery
from google.cloud import storage


def get_file_dates(file_path):
    pattern = (
        r"sf311_"
        r"(\d{4}-\d{2}-\d{2})_"
        r"(\d{4}-\d{2}-\d{2})"
        r"\.jsonl\.gz"
    )

    match = re.fullmatch(
        pattern,
        Path(file_path).name
    )

    if not match:
        raise ValueError(
            "Expected filename like "
            "sf311_2026-07-01_2026-08-01.jsonl.gz"
        )

    return match.group(1), match.group(2)


def count_rows(file_path):
    with gzip.open(
        file_path,
        "rt",
        encoding="utf-8"
    ) as file:
        return sum(1 for _ in file)


def build_object_name(file_path, start_date):
    year = start_date[:4]
    month = start_date[5:7]

    return (
        f"sf311/historical/"
        f"{year}/{month}/"
        f"{Path(file_path).name}"
    )


def upload_to_gcs(
    storage_client,
    bucket_name,
    file_path,
    object_name
):
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(object_name)

    print(
        f"Uploading to "
        f"gs://{bucket_name}/{object_name}"
    )

    blob.upload_from_filename(file_path)

    return (
        f"gs://{bucket_name}/"
        f"{object_name}"
    )


def already_loaded(
    bq_client,
    project_id,
    source_file
):
    query = f"""
        SELECT COUNT(*) AS successful_runs
        FROM `{project_id}.opspilot_raw.pipeline_runs`
        WHERE source_file = @source_file
          AND status = 'success'
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "source_file",
                "STRING",
                source_file
            )
        ]
    )

    result = bq_client.query(
        query,
        job_config=job_config
    ).result()

    row = next(result)

    return row.successful_runs > 0


def load_to_bigquery(
    bq_client,
    project_id,
    gcs_uri
):
    table_id = (
        f"{project_id}."
        f"opspilot_raw."
        f"sf311_cases_raw"
    )

    job_config = bigquery.LoadJobConfig(
        source_format=(
            bigquery.SourceFormat
            .NEWLINE_DELIMITED_JSON
        ),
        autodetect=True,
        write_disposition=(
            bigquery.WriteDisposition
            .WRITE_APPEND
        ),
        schema_update_options=[
            bigquery.SchemaUpdateOption
            .ALLOW_FIELD_ADDITION
        ]
    )

    print(
        f"Loading {gcs_uri} "
        f"into {table_id}"
    )

    load_job = bq_client.load_table_from_uri(
        gcs_uri,
        table_id,
        job_config=job_config
    )

    load_job.result()

    return load_job


def record_pipeline_run(
    bq_client,
    project_id,
    run_info
):
    table_id = (
        f"{project_id}."
        f"opspilot_raw."
        f"pipeline_runs"
    )

    errors = bq_client.insert_rows_json(
        table_id,
        [run_info]
    )

    if errors:
        raise RuntimeError(
            f"Failed to record pipeline run: "
            f"{errors}"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Upload an SF311 raw file "
            "to GCS and BigQuery."
        )
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Local .jsonl.gz file"
    )

    parser.add_argument(
        "--project-id",
        required=True,
        help="Google Cloud project ID"
    )

    parser.add_argument(
        "--bucket",
        required=True,
        help="Cloud Storage bucket name"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    file_path = Path(args.file)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    start_date, end_date = get_file_dates(
        file_path
    )

    expected_rows = count_rows(
        file_path
    )

    object_name = build_object_name(
        file_path,
        start_date
    )

    gcs_uri = (
        f"gs://{args.bucket}/"
        f"{object_name}"
    )

    storage_client = storage.Client(
        project=args.project_id
    )

    bq_client = bigquery.Client(
        project=args.project_id
    )

    if already_loaded(
        bq_client,
        args.project_id,
        gcs_uri
    ):
        print(
            "This file already has a "
            "successful load record."
        )
        print("Skipping.")
        return

    run_id = str(uuid.uuid4())

    started_at = datetime.now(
        timezone.utc
    )

    print("Starting cloud raw load")
    print(f"File: {file_path}")
    print(f"Rows expected: {expected_rows:,}")
    print(
        f"Date range: "
        f"{start_date} to {end_date}"
    )

    try:
        uploaded_uri = upload_to_gcs(
            storage_client,
            args.bucket,
            file_path,
            object_name
        )

        load_job = load_to_bigquery(
            bq_client,
            args.project_id,
            uploaded_uri
        )

        rows_loaded = (
            load_job.output_rows or 0
        )

        if rows_loaded != expected_rows:
            raise RuntimeError(
                f"Row-count mismatch. "
                f"Expected {expected_rows:,}, "
                f"loaded {rows_loaded:,}."
            )

        completed_at = datetime.now(
            timezone.utc
        )

        run_info = {
            "run_id": run_id,
            "pipeline_name": (
                "sf311_raw_cloud_load"
            ),
            "source_file": uploaded_uri,
            "source_start_date": start_date,
            "source_end_date": end_date,
            "rows_expected": expected_rows,
            "rows_loaded": rows_loaded,
            "started_at": (
                started_at.isoformat()
            ),
            "completed_at": (
                completed_at.isoformat()
            ),
            "status": "success",
            "error_message": None
        }

        record_pipeline_run(
            bq_client,
            args.project_id,
            run_info
        )

        print()
        print("Cloud load complete")
        print(f"Rows loaded: {rows_loaded:,}")
        print(f"Source: {uploaded_uri}")

    except Exception as error:
        completed_at = datetime.now(
            timezone.utc
        )

        run_info = {
            "run_id": run_id,
            "pipeline_name": (
                "sf311_raw_cloud_load"
            ),
            "source_file": gcs_uri,
            "source_start_date": start_date,
            "source_end_date": end_date,
            "rows_expected": expected_rows,
            "rows_loaded": 0,
            "started_at": (
                started_at.isoformat()
            ),
            "completed_at": (
                completed_at.isoformat()
            ),
            "status": "failed",
            "error_message": str(error)
        }

        record_pipeline_run(
            bq_client,
            args.project_id,
            run_info
        )

        raise


if __name__ == "__main__":
    main()