-- Portfolio example: load CSVs into RAW tables using an internal stage.
-- In a real setup, data would land in cloud storage and be copied in via external stage.

USE DATABASE FLEET_MONITORING;
USE SCHEMA RAW;

-- Example raw tables (adjust columns to match your generated CSVs if needed)
CREATE OR REPLACE TABLE RAW.FLIGHTS (
  week DATE,
  region STRING,
  model STRING,
  flights_total NUMBER,
  flights_success NUMBER,
  reliability_pct FLOAT,
  critical_events_per_100_flights FLOAT
);

-- (Optional) Create a stage and load
-- CREATE OR REPLACE STAGE RAW.DATA_STAGE;

-- COPY INTO RAW.FLIGHTS
-- FROM @RAW.DATA_STAGE/weekly_metrics.csv
-- FILE_FORMAT = (TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);
