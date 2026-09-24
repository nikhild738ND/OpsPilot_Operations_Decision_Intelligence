-- Basic checks after loading an SF311 raw file into BigQuery.

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT service_request_id) AS unique_request_ids,
    COUNTIF(service_request_id IS NULL) AS missing_request_ids,
    COUNTIF(requested_datetime IS NULL) AS missing_request_dates,
    MIN(requested_datetime) AS first_request,
    MAX(requested_datetime) AS last_request
FROM `opspilot-509616.opspilot_raw.sf311_cases_raw`;

-- Quick look at the largest service categories in the loaded data.

SELECT
    service_name,
    COUNT(*) AS requests
FROM `opspilot-509616.opspilot_raw.sf311_cases_raw`
GROUP BY service_name
ORDER BY requests DESC
LIMIT 20;