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