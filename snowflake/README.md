# Snowflake warehouse layer (portfolio)

This folder contains Snowflake-ready SQL scripts showing how this project would be modeled in a warehouse:

- RAW: ingested logs (events, flights, maintenance, routes, vehicles)
- CLEAN: standardized types + cleaned columns
- ANALYTICS: curated marts for dashboards (weekly_metrics, event_type_summary)

This is a portfolio implementation using simulated CSVs.

## Run order
1. 01_setup.sql
2. 02_stage_load.sql
3. 03_marts.sql
