-- Example marts for analytics (what Power BI would connect to)

USE DATABASE FLEET_MONITORING;
USE SCHEMA ANALYTICS;

-- Weekly metrics mart (already close to your CSV)
CREATE OR REPLACE VIEW ANALYTICS.WEEKLY_METRICS AS
SELECT
  week,
  region,
  model,
  flights_total,
  flights_success,
  reliability_pct,
  critical_events_per_100_flights
FROM FLEET_MONITORING.RAW.FLIGHTS;

-- Event type drivers mart (illustrative)
-- In a real system this would come from RAW.EVENTS logs.
