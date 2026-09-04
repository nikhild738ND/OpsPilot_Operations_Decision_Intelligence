# OpsPilot Requirements

## 1. Project Goal

OpsPilot is an operations analytics project built using San Francisco 311 service-request data.

The goal is to help an operations team answer four main questions:

1. What is happening with incoming requests, resolutions, and backlog?
2. Why is performance getting better or worse?
3. What workload should we expect over the next few days?
4. If capacity is limited, where should resources be allocated?

The project will start with operational reporting and gradually add forecasting, capacity planning, optimization, deployment, and monitoring.

## 2. Business Problem

Service-request volume changes every day.

Some days have normal demand, while other days may see a large increase in certain types of requests or neighborhoods.

If incoming work grows faster than the team can resolve it, backlog increases and requests remain open for longer.

A manager needs more than a dashboard showing what happened yesterday.

They need to know:

- where workload is increasing;
- which service areas are falling behind;
- why backlog is growing;
- how much demand is expected next;
- where capacity may become insufficient;
- what action could improve the situation.

OpsPilot will be built around those decisions.

## 3. Users

### Operations Manager

Needs to understand:

- current request volume;
- backlog;
- aging work;
- problem service categories;
- future workload;
- possible capacity shortages.

Main decision:

> Where does the team need more attention or capacity?

### Analyst

Needs to:

- calculate consistent KPIs;
- investigate changes;
- identify the biggest contributors to backlog or resolution problems;
- compare performance over time.

Main decision:

> What changed and what caused it?

### Workforce / Capacity Planner

Needs to understand:

- expected future demand;
- estimated workload;
- available capacity;
- possible capacity gaps.

Main decision:

> How much capacity will be needed and where?

### Leadership

Needs a simple summary of:

- current performance;
- major risks;
- expected future problems;
- recommended actions.

## 4. Questions the Project Should Answer

### Current Performance

- How many requests are coming in each day?
- How many requests are being closed?
- How many requests are still open?
- How quickly are requests being resolved?
- Which service categories receive the most requests?
- Which neighborhoods generate the most requests?

### Backlog

- Is backlog increasing or decreasing?
- Which categories contribute most to backlog?
- How old are unresolved requests?
- Where is backlog growing fastest?

### Root Cause

- Why did request volume increase?
- Why did backlog increase?
- Did incoming demand increase?
- Did resolution throughput decrease?
- Which categories or neighborhoods caused most of the change?

### Forecasting

- How many requests should we expect tomorrow?
- What should we expect over the next 7 days?
- Which service areas are likely to experience unusually high demand?

### Capacity

- How much workload is expected?
- How much capacity would be needed to handle it?
- Which areas are likely to have a capacity shortage?

### Decisions

- If capacity is limited, where should it go first?
- What happens if demand increases?
- What happens if available capacity decreases?
- Can a different allocation reduce backlog or service risk?

## 5. Initial Scope

The first complete version of OpsPilot should include:

- SF311 data ingestion;
- historical data storage;
- incremental data updates;
- BigQuery data warehouse;
- dbt transformations;
- data-quality checks;
- daily operations KPIs;
- backlog analysis;
- resolution-time analysis;
- root-cause analysis;
- Tableau dashboard;
- demand forecasting;
- forecast backtesting;
- capacity calculations;
- scenario analysis;
- resource-allocation optimization;
- API for selected outputs;
- Docker deployment;
- basic monitoring;
- GitHub Actions for testing/deployment.

Not everything will be built at once.

Each part will be added after the previous layer is working.

## 6. Out of Scope

This project will not:

- claim to represent San Francisco's actual staffing process;
- use private employee data;
- make real staffing decisions for the City of San Francisco;
- claim real financial savings unless they can actually be measured;
- claim that simulated capacity numbers are real government workforce numbers.

SF311 provides the operational request data.

Capacity, staffing, and cost inputs that are not available from the dataset will be clearly labeled as project assumptions.

## 7. Main Metrics

The first analytics layer should eventually calculate:

### Incoming Requests

Number of new service requests created during a period.

### Resolved Requests

Number of service requests closed during a period.

### Open Backlog

Number of service requests that remain unresolved.

### Backlog Change

Change in backlog compared with the previous period.

### Resolution Time

Time between request creation and closure.

We will look at:

- median;
- average;
- P90.

### Backlog Age

How long currently open requests have been waiting.

Possible groups:

- less than 1 day;
- 1–3 days;
- 3–7 days;
- 7–14 days;
- more than 14 days.

These groups may change after we inspect the real data.

### Forecast Demand

Expected number of future requests.

### Capacity Gap

Conceptually:

required capacity - available capacity

A positive value means additional capacity may be required.

## 8. Data Requirements

The source data should contain enough information to identify:

- individual service requests;
- when a request was created;
- when it was closed;
- current status;
- service category;
- service subtype where available;
- responsible agency;
- neighborhood/location;
- request source;
- last update time.

Before using any field, we will first inspect the actual source data and confirm what it contains.

We will not build calculations around fields that do not actually exist.

## 9. Data Quality Requirements

Before data reaches reporting or modeling tables, we should check for:

- duplicate request IDs;
- missing request IDs;
- missing request timestamps;
- invalid dates;
- closed dates earlier than request dates;
- unexpected status values;
- large changes in row counts;
- stale source data.

A failed important data-quality check should be visible rather than silently ignored.

## 10. Forecasting Requirements

Forecasting will be added only after the historical analytics layer is working.

The project should:

- start with a simple baseline;
- evaluate forecasts using historical backtesting;
- compare more advanced models with the baseline;
- avoid using future information when creating features;
- measure forecast error over multiple historical periods.

Possible forecast horizons:

- next day;
- next 7 days;
- next 14 days.

A 28-day horizon may be added if the data supports it.

The final model will be selected based on results, not because one algorithm looks more impressive.

## 11. Capacity Planning Requirements

The SF311 dataset does not contain a complete workforce-planning system.

Because of that, capacity planning will use clearly documented assumptions.

Examples may include:

- workload handled per capacity unit;
- available capacity by service group;
- maximum extra capacity;
- operating cost assumptions.

These will be kept separate from observed SF311 data.

The capacity model should estimate:

- expected workload;
- available capacity;
- required capacity;
- shortages or surpluses.

## 12. Optimization Requirements

After forecasting and capacity planning are working, the project should test whether available capacity can be allocated more effectively.

The optimizer should:

- work within total available capacity;
- respect minimum coverage where required;
- avoid impossible allocations;
- return a feasible recommendation;
- make its assumptions visible.

The goal is not to make a perfect real-world staffing model.

The goal is to demonstrate how forecasts can be turned into a constrained business decision.

## 13. Scenario Analysis

A user should eventually be able to test simple scenarios such as:

- demand increases by 10%;
- demand increases by 20%;
- available capacity decreases by 10%;
- one service category experiences a demand spike.

The system should recalculate expected:

- workload;
- capacity gap;
- backlog risk;
- recommended allocation.

## 14. Dashboard Requirements

The dashboard should focus on decisions rather than showing as many charts as possible.

The main views should eventually cover:

### Operations Overview

- incoming requests;
- resolved requests;
- backlog;
- resolution time;
- trends.

### Backlog and Root Cause

- backlog by category;
- backlog age;
- largest contributors to change.

### Forecast and Capacity

- future demand;
- forecast range;
- required versus available capacity.

### Scenario / Recommendation

- scenario assumptions;
- expected impact;
- recommended allocation.

## 15. Production Requirements

The final project should not depend only on notebooks.

Production logic should eventually live in:

- Python files;
- SQL files;
- dbt models;
- tested APIs.

The project should eventually include:

- automated ingestion;
- scheduled transformations;
- data tests;
- model evaluation;
- API health check;
- Docker container;
- deployment;
- monitoring;
- CI/CD.

These will be added gradually.

## 16. Assumptions

At the start of the project, we are making only a few assumptions:

1. SF311 data can represent a realistic service-operations use case.
2. Historical request volume contains enough structure to test forecasting.
3. Workforce capacity is not fully available from the public dataset.
4. Capacity-related values will therefore be modeled separately.
5. The project is for analytical demonstration and will not control real operational resources.

These assumptions can be updated as we learn more about the data.

## 17. Success Criteria

The project will be considered successful if we can demonstrate the following workflow:

SF311 data
↓
clean operational tables
↓
reliable KPIs
↓
backlog and root-cause analysis
↓
future demand forecast
↓
capacity-gap estimate
↓
allocation recommendation
↓
deployed output

More specifically:

- historical data loads successfully;
- new records can be loaded incrementally;
- important data-quality problems are detected;
- KPI calculations are reproducible;
- backlog changes can be explained using data;
- forecasting is compared against a simple baseline;
- capacity calculations use transparent assumptions;
- optimization recommendations respect constraints;
- selected results are available through a deployed application/API;
- the repository contains enough documentation for another analyst to understand how the project works.

## 18. What We Will Measure Later

We will not invent project-impact numbers at the beginning.

After the system is working, we will calculate real results such as:

- forecast improvement over baseline;
- forecast error;
- percentage of periods with correct demand direction;
- simulated backlog reduction;
- simulated service improvement;
- optimizer improvement over a simple allocation rule;
- pipeline success rate;
- data-quality test coverage.

Only measured results will be used in the README and resume.
