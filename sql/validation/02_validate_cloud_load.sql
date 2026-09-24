-- Recent cloud ingestion runs.

SELECT
    source_start_date,
    source_end_date,
    rows_expected,
    rows_loaded,
    status,
    started_at,
    completed_at,
    error_message
FROM `opspilot-509616.opspilot_raw.pipeline_runs`
ORDER BY started_at DESC;


-- Check loaded monthly counts.

SELECT
    DATE_TRUNC(
        DATE(
            SAFE_CAST(
                requested_datetime AS TIMESTAMP
            )
        ),
        MONTH
    ) AS request_month,
    COUNT(*) AS requests
FROM `opspilot-509616.opspilot_raw.sf311_cases_raw`
GROUP BY request_month
ORDER BY request_month;