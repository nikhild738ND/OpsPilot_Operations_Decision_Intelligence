# OpsPilot Business Problem

## Background
Large service organizations process thousands or millions of operational
requests across different service categories, geographic areas, teams,
and channels.

Request demand changes continuously, while staffing, time, budget, and
processing capacity remain limited.

Operations leaders therefore need to understand not only historical
performance, but also emerging operational risk, future demand,
capacity requirements, and the actions required to maintain reliable
service performance.

OpsPilot is designed as an enterprise service-operations decision
intelligence platform demonstrated using real San Francisco 311
service-request data.

## Business Problem
Large service organizations receive continuously changing volumes of
operational requests while working with limited staffing, budget, and
processing capacity.

Traditional reporting systems primarily describe historical performance,
such as request volume, backlog, and resolution time, but provide limited
support for anticipating future operational risk or determining how
resources should be allocated.

This creates several business challenges:

- sudden increases in demand may not be identified early enough;
- growing backlogs may cause service-level deterioration;
- managers may not know which service queues are responsible for
  performance declines;
- workforce and capacity planning may rely heavily on manual estimates;
- operational resources may be allocated inefficiently across queues;
- decision-makers may lack a reliable way to evaluate what-if scenarios
  before changing staffing or capacity.

OpsPilot addresses this problem by building a production decision-intelligence
platform that continuously measures operational performance, identifies
the root causes of deterioration, forecasts future demand, estimates
service-level risk, calculates required capacity, simulates operational
scenarios, and recommends resource allocations subject to business
constraints.

The platform uses real San Francisco 311 service-request data as a
public-data representation of a large-scale service-operations environment.

## Business Objective
The objective of OpsPilot is to help operations leaders maintain reliable
service performance under changing demand and limited capacity by providing
timely operational measurement, root-cause analysis, demand forecasting,
service-risk prediction, capacity planning, scenario simulation, and
constrained resource-allocation recommendations.

The platform should enable decision-makers to detect operational deterioration
earlier, understand its drivers, evaluate possible responses, and select
feasible actions using consistent and auditable analytics.

## Current State
The current operating process is largely reactive.

Requests arrive
↓
Requests accumulate
↓
Managers inspect dashboards
↓
Performance deteriorates
↓
Manager notices the problem
↓
Manual investigation begins
↓
Manual staffing or capacity decision is made

The main limitation of this approach is that managers often respond after
service performance has already deteriorated.

## Target State
OpsPilot is designed to support a proactive operating model.

Requests arrive
↓
Automated ingestion
↓
Operational KPIs calculated
↓
Anomalies detected
↓
Root cause identified
↓
Future demand forecast
↓
SLA and capacity risk calculated
↓
Optimization engine recommends action
↓
Manager reviews recommendation
↓
Approve / Modify / Reject
↓
Outcome monitored

The target state shifts operations from a reactive model to a proactive
decision process in which emerging risks can be identified and evaluated
before service performance deteriorates significantly.

## Stakeholders
### VP of Operations

Key decisions:

- Are service targets being met?
- Where is operational risk increasing?
- What decisions require management attention?

### Operations Manager

Key decisions:

- Which service queue is overloaded?
- Where should additional capacity be moved?
- Which requests should receive priority?

### Workforce Planner

Key decisions:

- How much future demand is expected?
- How much capacity will be required?
- Where will staffing or capacity gaps occur?

### Finance

Key decisions:

- What will additional capacity cost?
- What happens if available capacity is reduced?
- What is the lowest-cost feasible operating plan?

### Business/Data Analyst

Key decisions:

- What caused operational performance to change?
- Which categories contributed to the change?
- Which geographic areas contributed?
- Was the problem caused by increased demand or reduced throughput?

### Leadership

Key decisions:

- What happened?
- Why did it happen?
- What is likely to happen next?
- What should we do?

## Analytical Questions
### Descriptive

1. How many requests are created every day?
2. How many requests are resolved every day?
3. How large is the open backlog?
4. How old is the backlog?
5. How long do requests take to resolve?
6. Which service categories have the highest demand?
7. Which areas generate the most requests?
8. Which channels generate requests?

### Diagnostic

9. Why did backlog increase?
10. Why did resolution performance deteriorate?
11. Which service category contributed most?
12. Which neighborhood contributed most?
13. Was deterioration caused primarily by higher incoming demand or lower resolution throughput?
14. Is the performance change normal seasonality or unusual behavior?

### Predictive

15. How many requests should we expect tomorrow?
16. How many requests should we expect next week?
17. Which queues are likely to experience unusual demand?
18. Which open requests are likely to become high risk?
19. Which service queues are likely to experience insufficient capacity?

### Prescriptive

20. Where should resources be allocated?
21. Which queues should receive additional capacity?
22. Which cases should receive priority?
23. How much capacity is required to maintain the target?
24. What is the lowest-cost allocation that satisfies operational constraints?

### Scenario Simulation

25. What if demand increases 10%?
26. What if demand increases 25%?
27. What if available capacity drops 15%?
28. What if service targets become stricter?
29. What happens under a severe-demand scenario?
30. What combination of resources produces the best operating outcome?

## Success Criteria
### Data Success

The system should:

- ingest new data automatically;
- avoid duplicate records;
- identify missing or invalid records;
- track pipeline executions;
- detect stale data.

### Analytics Success

The system should consistently calculate centralized definitions for:

- request volume;
- backlog;
- resolution time;
- service performance;
- backlog aging;
- queue health.

### Forecasting Success

Future forecasting models should:

- outperform a defined baseline;
- maintain acceptable forecasting bias;
- produce useful uncertainty ranges.

Exact thresholds will be determined after exploratory data analysis and should not be invented before understanding the data.

### Decision Success

The optimization engine should produce feasible recommendations that obey all defined operational constraints.

Optimized decisions will later be compared against baseline resource-allocation strategies.

### Production Success

The deployed platform should include:

- automated pipelines;
- automated tests;
- monitoring;
- versioning;
- health checks;
- deployment workflows.

### Business Success

Managers should be able to move from:

metric deterioration  
↓  
root cause  
↓  
future risk  
↓  
recommended action

without performing separate manual analyses.

## Assumptions
OpsPilot uses two categories of information: observed data and simulation assumptions.

### Observed Data

Observed data is information actually available in the San Francisco 311 public dataset.

Examples include:

- service requests;
- timestamps;
- service category;
- request status;
- neighborhood;
- responsible agency.

### Simulation Assumptions

Some information required for capacity planning, workforce modeling, and optimization is not available in the SF311 public dataset.

Therefore, OpsPilot may introduce explicitly documented modeling assumptions such as:

- capacity per worker;
- hourly capacity cost;
- maximum overtime;
- queue staffing;
- service targets;
- operational resource constraints.

These variables must always be labeled as simulation assumptions and must not be represented as actual San Francisco staffing, workforce, wage, or internal operational data.

## Non-Goals
OpsPilot is not intended to reproduce or claim to replace the City and County of San Francisco's actual operational planning processes.

The project does not claim access to private staffing, workforce, labor-cost, scheduling, or internal service-level data.

Where operational capacity, staffing cost, service targets, or resource constraints are required for simulation and optimization, these inputs will be explicitly documented as modeling assumptions.

The project's purpose is to demonstrate an enterprise-grade analytics and decision-intelligence architecture using real public service-request data.
