# Fleet Monitoring Analytics (SQL + Snowflake + Power BI + Python)

This project simulates a systems engineering analytics stack for **system health monitoring**:
- Generate / ingest raw event logs (flights, events, maintenance)
- Compute **reliability + safety metrics** using SQL (joins, aggregations, window functions)
- Model data in a **warehouse** (Snowflake: RAW → CLEAN → ANALYTICS marts)
- Build a **Power BI monitoring dashboard** with drilldowns + alert thresholds
- Run **Python** anomaly detection and generate an incident report

## What you’ll find here
- `sql/` — SQL schema + metric queries (reliability, safety, incident rates)
- `snowflake/` — warehouse scripts and curated marts
- `powerbi/` — dashboard file and exports
- `python/` — notebooks + scripts (data generation, anomaly detection)
- `data/` — generated and cleaned CSVs (small sample only)

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
