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


def validate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start >= end:
        raise ValueError(
            "end-date must be later than start-date"
        )


def build_output_path(start_date, end_date):
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = (
        f"sf311_{start_date}_{end_date}.jsonl.gz"
    )

    return output_dir / filename


def download_date_range(
    start_date,
    end_date,
    output_path
):
    offset = 0
    row_count = 0

    temp_path = Path(str(output_path) + ".tmp")

    try:
        with gzip.open(
            temp_path,
            "wt",
            encoding="utf-8"
        ) as file:

            while True:
                params = {
                    "$where": (
                        f"requested_datetime >= "
                        f"'{start_date}T00:00:00' "
                        f"AND requested_datetime < "
                        f"'{end_date}T00:00:00'"
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

                for record in page:
                    file.write(json.dumps(record))
                    file.write("\n")

                row_count += len(page)

                print(
                    f"Fetched {len(page):,} rows "
                    f"| total: {row_count:,}"
                )

                if len(page) < BATCH_SIZE:
                    break

                offset += BATCH_SIZE

        temp_path.replace(output_path)

        return row_count

    except Exception:
        if temp_path.exists():
            temp_path.unlink()

        raise


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download one range of SF311 data."
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

    output_path = build_output_path(
        args.start_date,
        args.end_date
    )

    print("Starting SF311 download")
    print(
        f"Date range: "
        f"{args.start_date} to {args.end_date}"
    )

    row_count = download_date_range(
        args.start_date,
        args.end_date,
        output_path
    )

    print()
    print("Download complete")
    print(f"Rows: {row_count:,}")
    print(f"File: {output_path}")


if __name__ == "__main__":
    main()