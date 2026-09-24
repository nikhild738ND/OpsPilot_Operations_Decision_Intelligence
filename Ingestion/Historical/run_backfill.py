import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path

from load_sf311 import (
    build_output_path,
    download_date_range,
    validate_dates
)


CHECKPOINT_PATH = Path(
    "data/checkpoints/historical_backfill.json"
)


def parse_date(value):
    return datetime.strptime(
        value,
        "%Y-%m-%d"
    ).date()


def next_month(value):
    if value.month == 12:
        return date(
            value.year + 1,
            1,
            1
        )

    return date(
        value.year,
        value.month + 1,
        1
    )


def build_chunks(start_date, end_date):
    current = start_date

    while current < end_date:
        month_end = next_month(current)

        chunk_end = min(
            month_end,
            end_date
        )

        yield current, chunk_end

        current = chunk_end


def load_checkpoint():
    if not CHECKPOINT_PATH.exists():
        return {
            "completed_chunks": {}
        }

    with open(
        CHECKPOINT_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_checkpoint(checkpoint):
    CHECKPOINT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = Path(
        str(CHECKPOINT_PATH) + ".tmp"
    )

    with open(
        temp_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            checkpoint,
            file,
            indent=2
        )

    temp_path.replace(CHECKPOINT_PATH)


def chunk_key(start_date, end_date):
    return (
        f"{start_date.isoformat()}_"
        f"{end_date.isoformat()}"
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run SF311 historical backfill "
            "in monthly chunks."
        )
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

    start_date = parse_date(
        args.start_date
    )

    end_date = parse_date(
        args.end_date
    )

    checkpoint = load_checkpoint()

    print("Starting SF311 historical backfill")
    print(
        f"Range: {start_date} to {end_date}"
    )
    print()

    for chunk_start, chunk_end in build_chunks(
        start_date,
        end_date
    ):
        key = chunk_key(
            chunk_start,
            chunk_end
        )

        start_text = chunk_start.isoformat()
        end_text = chunk_end.isoformat()

        output_path = build_output_path(
            start_text,
            end_text
        )

        completed = checkpoint[
            "completed_chunks"
        ].get(key)

        if completed and output_path.exists():
            print(
                f"Skipping {start_text} "
                f"to {end_text} "
                f"(already complete)"
            )
            continue

        if output_path.exists():
            print(
                f"Existing file found without "
                f"checkpoint entry: {output_path}"
            )
            print("Removing and downloading again.")

            output_path.unlink()

        print()
        print(
            f"Loading {start_text} "
            f"to {end_text}"
        )

        row_count = download_date_range(
            start_text,
            end_text,
            output_path
        )

        checkpoint[
            "completed_chunks"
        ][key] = {
            "rows": row_count,
            "file": str(output_path),
            "completed_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        save_checkpoint(checkpoint)

        print(
            f"Finished chunk "
            f"| rows: {row_count:,}"
        )

    print()
    print("Historical backfill complete.")


if __name__ == "__main__":
    main()