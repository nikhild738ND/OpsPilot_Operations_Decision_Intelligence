import argparse
import gzip
import json
import time
from datetime import datetime
from pathlib import Path

import requests


API_URL = "https://data.sfgov.org/resource/vw6y-z8j6.json"

BATCH_SIZE = 5000
MAX_RETRIES = 3


def fetch_page(params):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=60
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            print(
                f"Request failed "
                f"(attempt {attempt}/{MAX_RETRIES}): "
                f"{error}"
            )

            if attempt == MAX_RETRIES:
                raise

            time.sleep(2 * attempt)


def fetch_historical_data(start_date, end_date):
    records = []
    offset = 0

    while True:
        params = {
            "$where": (
                f"requested_datetime >= '{start_date}T00:00:00' "
                f"AND requested_datetime < '{end_date}T00:00:00'"
            ),
            "$order": (
                "requested_datetime ASC, "
                "service_request_id ASC"
            ),
            "$limit": BATCH_SIZE,
            "$offset": offset
        }

        page = fetch_page(params)

        if not page:
            break

        records.extend(page)

        print(
            f"Fetched {len(page):,} rows "
            f"| total: {len(records):,}"
        )

        if len(page) < BATCH_SIZE:
            break

        offset += BATCH_SIZE

    return records


def save_raw_data(records, start_date, end_date):
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = (
        f"sf311_"
        f"{start_date}_"
        f"{end_date}.jsonl.gz"
    )

    output_path = output_dir / filename

    with gzip.open(
        output_path,
        "wt",
        encoding="utf-8"
    ) as file:
        for record in records:
            file.write(json.dumps(record))
            file.write("\n")

    return output_path


def save_run_summary(
    start_date,
    end_date,
    row_count,
    output_path,
    started_at,
    completed_at
):
    log_dir = Path("data/run_logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    run_timestamp = started_at.strftime(
        "%Y%m%d_%H%M%S"
    )

    log_path = (
        log_dir
        / f"historical_load_{run_timestamp}.json"
    )

    run_info = {
        "pipeline": "sf311_historical_load",
        "start_date": start_date,
        "end_date": end_date,
        "rows_extracted": row_count,
        "output_file": str(output_path),
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "status": "success"
    }

    with open(
        log_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            run_info,
            file,
            indent=2
        )

    return log_path


def validate_dates(start_date, end_date):
    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    if start >= end:
        raise ValueError(
            "end-date must be later than start-date"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download historical SF311 data."
    )

    parser.add_argument(
        "--start-date",
        required=True,
        help="Start date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--end-date",
        required=True,
        help="End date in YYYY-MM-DD format"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    validate_dates(
        args.start_date,
        args.end_date
    )

    started_at = datetime.now()

    print("Starting SF311 historical load")
    print(
        f"Date range: "
        f"{args.start_date} to {args.end_date}"
    )

    records = fetch_historical_data(
        args.start_date,
        args.end_date
    )

    if not records:
        print("No records returned.")
        return

    output_path = save_raw_data(
        records,
        args.start_date,
        args.end_date
    )

    completed_at = datetime.now()

    log_path = save_run_summary(
        start_date=args.start_date,
        end_date=args.end_date,
        row_count=len(records),
        output_path=output_path,
        started_at=started_at,
        completed_at=completed_at
    )

    print()
    print("Load complete")
    print(f"Rows: {len(records):,}")
    print(f"Raw file: {output_path}")
    print(f"Run log: {log_path}")


if __name__ == "__main__":
    main()