# Cloud Setup

OpsPilot currently uses Google Cloud for raw storage and the data warehouse.

## Resources

Google Cloud project:
`opspilot-509616`

Cloud Storage bucket:
`opspilot-raw-opspilot-509616`

BigQuery datasets:

- `opspilot_raw`
- `opspilot_analytics`

Location:
`US`

## Current Flow

SF311 API
→ local historical ingestion
→ compressed JSONL
→ Cloud Storage
→ BigQuery raw table

The first BigQuery load was done manually so I could verify the source format,
schema, and row counts before automating cloud ingestion.

## Automated Raw Load

Historical files can now be uploaded and loaded from the command line.

Example:

```bash
python Ingestion/cloud/load_raw_to_gcp.py \
  --file data/raw/sf311_2026-07-01_2026-08-01.jsonl.gz \
  --project-id <project-id> \
  --bucket <raw-bucket>
```

The script:

1. counts the records in the local JSONL file;
2. uploads the compressed file to Cloud Storage;
3. loads the file into `opspilot_raw.sf311_cases_raw`;
4. checks that the BigQuery load count matches the local file;
5. writes the load result to `opspilot_raw.pipeline_runs`.

Successful files are skipped on later runs to avoid accidental duplicate loads.