# Fleet Monitoring Analytics (SQL + Snowflake + Power BI + Python)

This project simulates a systems engineering analytics stack for **system health monitoring**:
- Generate / ingest raw event logs (flights, events, maintenance)
- Compute **reliability + safety metrics** using SQL (joins, aggregations, window functions)
- Model data in a **warehouse** (Snowflake: RAW → CLEAN → ANALYTICS marts)
- Build a **Power BI monitoring dashboard** with drilldowns + alert thresholds
- Run **Python** anomaly detection and generate an incident report

📌 Metrics reference: [docs/metrics_definition.md](docs/metrics_definition.md)

## What you’ll find here
- `sql/` — SQL schema + metric queries (reliability, safety, incident rates)
- `snowflake/` — warehouse scripts and curated marts
- `powerbi/` — dashboard file and exports
- `python/` — notebooks + scripts (data generation, anomaly detection)
- `data/` — generated and cleaned CSVs (small sample only)

## Dashboard preview
<img src="powerbi/screenshots/overview_dashboard.png" alt="Fleet system health dashboard overview" width="480" />

### What this dashboard answers
- Fleet reliability (success rate) trend over time
- Safety signal via critical events per 100 flights
- Which regions are most at risk
- How reliability differs by region and vehicle model

### Key definitions (simple)
- Reliability (Weighted) = successful flights ÷ total flights
- Critical events per 100 flights = (critical events ÷ total flights) × 100
- Status thresholds: Good ≥ 95%, Watch 93–95%, Risk < 93%
- Target line: 95% reliability

### Vehicle model definitions (A, B, C)
The `model` field represents simulated platform variants:
- We have model A, model B, and model C. 

### Current findings (based on your current view)
- Overall reliability ≈ 94.75% → Watch (below 95% target)
- West and East are lowest reliability (top regions at risk)
- Safety trend fluctuates and rises near the end of the window → needs investigation

### Actions you’d take (systems thinking)
- Investigate weeks where reliability dips: correlate with event spikes
- Break down critical events by event type (comms loss, battery drop, etc.)
- Identify whether issues are model-specific or region-specific

## Drivers dashboard
<img src="powerbi/screenshots/drivers_page.png" alt="Critical event drivers dashboard" width="480" />
Critical Event Drivers: The highest driver of high/critical safety events is GPS Glitch (88 events in the current view), followed by Battery Drop and Motor Temp High. This view helps prioritize root-cause investigation by event type and segment findings by region/model via filters.

## Results
- Overall reliability is monitored weekly against a 95% target
- West/East show lower reliability in the current view (risk prioritization)
- GPS Glitch is the top critical event driver (drivers page)

## Key skills demonstrated (ATS keywords)
SQL · window functions · joins · aggregations · query optimization  
Snowflake · data warehouse · data models · curated marts  
Power BI · dashboarding · monitoring · alert thresholds · stakeholder reporting  
Python · pandas · numpy · matplotlib · Jupyter · anomaly detection

## Roadmap
1) Generate synthetic fleet logs (so the project is reproducible)  
2) Build SQL metrics + weekly reliability tables  
3) Create Snowflake warehouse layers + marts  
4) Build Power BI dashboard (exec + engineering views)  
5) Add Python anomaly detection feeding incidents back to analytics


## How to run the pipeline

Install dependencies, then run the one-command pipeline:

python python/src/run_all.py

This regenerates:
- data/raw/*.csv
- data/clean/*.csv
- data/outputs/weekly_metrics.csv (used by the Power BI dashboard)
