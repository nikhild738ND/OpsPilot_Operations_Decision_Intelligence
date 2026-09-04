# KPI Dictionary

This file keeps the main OpsPilot metrics in one place.

I am defining the metrics before building the dashboard so that the same calculation can be reused in SQL, dbt, Tableau, and later API outputs.

The definitions may change slightly after profiling the source data, but any changes should be documented here.

## Source

Dataset: San Francisco 311 Cases

Dataset ID:

`vw6y-z8j6`

The main source fields used for the first analytics layer are:

- `service_request_id`
- `requested_datetime`
- `closed_date`
- `updated_datetime`
- `status_description`
- `agency_responsible`
- `service_name`
- `service_subtype`
- `analysis_neighborhood`
- `supervisor_district`
- `source`

# 1. Incoming Requests

## What it means

Number of service requests opened during a selected period.

This is the main demand metric.

If 8,000 requests were opened on Monday, incoming requests for Monday = 8,000.

## Source fields

- `service_request_id`
- `requested_datetime`

## Calculation

Count distinct service request IDs based on the date the request was opened.

Conceptually:

`distinct requests opened during the period`

## Default grain

Daily.

Later we should also support:

- week;
- month;
- service category;
- neighborhood;
- agency.

## Important note

I want to use distinct request IDs instead of simply counting rows.

Before relying on this calculation, I will check whether duplicate `service_request_id` values exist in the raw data.

# 2. Resolved Requests

## What it means

Number of service requests closed during a selected period.

This represents completed work.

## Source fields

- `service_request_id`
- `closed_date`

## Calculation

Count distinct service request IDs where the closed date falls inside the selected period.

For example:

A request opened Monday and closed Thursday should count as:

- incoming volume on Monday;
- resolved volume on Thursday.

## Default grain

Daily.

## Important note

I do not want to calculate this using only `status_description = 'Closed'`.

The closing date is what tells us when the work was completed.

We will still validate that closed records and statuses make sense during data profiling.

# 3. Open Backlog

## What it means

Number of requests that were still unresolved at a specific point in time.

This is different from incoming volume.

A request may have arrived several days ago and still be part of today's backlog.

## Source fields

- `service_request_id`
- `requested_datetime`
- `closed_date`

## Calculation

For a reporting date, a request belongs to backlog when:

- it had already been opened by that date;
- and it had not been closed by that date.

Conceptually:

`requested_datetime <= reporting date`

and

`closed_date is null OR closed_date > reporting date`

## Example

Request A:

Opened: January 1  
Closed: January 5

It is part of the backlog at the end of:

- January 1;
- January 2;
- January 3;
- January 4.

It is no longer open after it closes on January 5.

## Important note

For today's current backlog, using records that are currently open may work.

For historical backlog, we cannot simply filter the current dataset to `status = Open`.

We need to reconstruct the backlog using the opened and closed dates.

This distinction is important because we eventually want historical backlog trends.

# 4. Backlog Change

## What it means

Shows whether outstanding work is increasing or decreasing.

## Calculation

`current backlog - previous backlog`

For daily reporting:

`today's backlog - yesterday's backlog`

## Interpretation

Positive value:

Backlog increased.

Negative value:

Backlog decreased.

Zero:

Backlog stayed the same.

## Example

Yesterday's backlog:

4,500

Today's backlog:

4,850

Backlog change:

`+350`

## Additional version

Later we can also calculate percentage change:

`(current backlog - previous backlog) / previous backlog`

I would keep both the absolute change and percentage change because they answer slightly different questions.

# 5. Resolution Time

## What it means

Amount of time between a service request being opened and being closed.

This tells us how long completed requests took to resolve.

## Source fields

- `requested_datetime`
- `closed_date`

## Calculation

`closed_date - requested_datetime`

Only closed requests should be included.

## Unit

I plan to calculate the base value in hours.

Hours are more flexible because they can later be converted into days where needed.

## Metrics to report

### Median Resolution Time

The middle resolution time.

This will probably be more useful than the average if a small number of requests remain open for a very long time.

### Average Resolution Time

Useful as a supporting metric, but it may be influenced by extreme values.

### P90 Resolution Time

90% of completed requests were resolved within this amount of time.

I want to include P90 because an average alone can hide slow cases.

## Data-quality rule

A valid resolution time cannot be negative.

If:

`closed_date < requested_datetime`

the record should be investigated instead of silently included.

# 6. Backlog Age

## What it means

How long currently unresolved requests have been waiting.

Resolution time looks at completed requests.

Backlog age looks at requests that are still open.

## Source fields

- `requested_datetime`
- `closed_date`

## Calculation

For an unresolved request:

`reporting time - requested_datetime`

For historical reporting, a request should only be considered open if it had not yet been closed as of that reporting date.

## Initial age groups

I will start with:

- less than 1 day;
- 1–3 days;
- 3–7 days;
- 7–14 days;
- more than 14 days.

These are starting buckets, not official SF311 service standards.

If the real data shows that these ranges are not useful, I will change them.

## Why it matters

Two queues can have the same backlog size but very different risk.

Example:

Queue A:

1,000 requests, mostly less than one day old.

Queue B:

1,000 requests, mostly more than seven days old.

Looking only at backlog count would make them look identical.

They are not.

# 7. Resolution Throughput

## What it means

Amount of work completed during a period.

For the first version, this will simply be the number of requests closed per day.

## Source fields

- `service_request_id`
- `closed_date`

## Calculation

`distinct requests closed during the period`

## Why keep this separate from Resolved Requests?

The underlying count is initially the same.

I am keeping the business idea of throughput because later the capacity model may use it to estimate how much work a service area historically handles.

For now, I do not need a separate physical column if it duplicates resolved volume.

# 8. Net Workload Change

## What it means

Simple comparison between new work arriving and work being completed.

## Calculation

`incoming requests - resolved requests`

## Interpretation

If the result is positive:

More work arrived than was completed.

This can put upward pressure on backlog.

If the result is negative:

More work was completed than arrived.

This can help reduce backlog.

## Example

Incoming:

5,200

Resolved:

4,700

Net workload change:

`+500`

This does not replace the actual historical backlog calculation, but it is useful for understanding why backlog may be moving.

# Dimensions

The KPIs should eventually be filterable or grouped using a small set of useful business dimensions.

## Service Category

Source:

`service_name`

Examples will be checked from the real data during exploration.

This will be one of the main ways we break down demand and backlog.

## Service Subtype

Source:

`service_subtype`

This gives a more detailed breakdown within a service category.

I will not use this everywhere because too much detail can make reporting noisy.

## Responsible Agency

Source:

`agency_responsible`

Useful for understanding which organization is responsible for handling the request.

## Analysis Neighborhood

Source:

`analysis_neighborhood`

This will be the main neighborhood field for analysis unless data profiling gives us a reason to use another geographic field.

## Supervisor District

Source:

`supervisor_district`

Useful for district-level reporting.

## Request Source

Source:

`source`

Shows how requests were submitted, such as phone, web, or mobile channels.

The actual values will be checked directly from the dataset.

# Metrics We Are Not Defining Yet

There are several metrics planned for OpsPilot that I do not want to define before understanding the data.

These include:

- SLA attainment;
- SLA breach rate;
- available capacity;
- required capacity;
- capacity gap;
- cost per capacity unit;
- forecast accuracy;
- forecast bias;
- predicted service risk;
- optimization savings.

These will be added later.

The reason is simple: some of them depend on modeling assumptions or models that do not exist yet.

I do not want to create fake business definitions just to make the KPI list larger.

# Current KPI List

| KPI | Main Purpose |
| --- | --- |
| Incoming Requests | Measure demand |
| Resolved Requests | Measure completed work |
| Open Backlog | Measure outstanding work |
| Backlog Change | Measure whether backlog is growing |
| Resolution Time | Measure how long completed requests take |
| Backlog Age | Measure how old unresolved work is |
| Resolution Throughput | Measure completion volume |
| Net Workload Change | Compare incoming work with completed work |

# A Few Rules I Want to Keep

## One definition per metric

If backlog is defined here one way, Tableau should not calculate it differently.

The same logic should eventually come from our SQL/dbt layer.

## Keep observed and modeled metrics separate

Incoming requests and resolution times come from the real dataset.

Future capacity and staffing calculations will use assumptions.

Those should never be mixed together without clear labels.

## Do not hide bad data

If a request has an impossible timestamp or another data problem, I want to identify it during testing rather than quietly change the record.

## Do not add metrics just because they look good on a dashboard

Every metric should answer a business question.

This file will be updated when new metrics are actually needed.
