-- event_type_summary.sql
-- Summarize events by type and severity so we can see what's driving safety risk.

WITH flights AS (
  SELECT * FROM read_csv_auto('data/clean/flights.csv')
),
events AS (
  SELECT * FROM read_csv_auto('data/clean/events.csv')
),

-- total flights in the dataset (for rate calculation)
flight_count AS (
  SELECT COUNT(*) AS total_flights
  FROM flights
),

event_summary AS (
  SELECT
    event_type,
    COUNT(*) AS total_events,
    SUM(CASE WHEN severity IN ('HIGH','CRITICAL') THEN 1 ELSE 0 END) AS critical_events
  FROM events
  GROUP BY 1
)

SELECT
  e.event_type,
  e.total_events,
  e.critical_events,
  ROUND(100.0 * e.critical_events / NULLIF(f.total_flights, 0), 2) AS critical_events_per_100_flights
FROM event_summary e
CROSS JOIN flight_count f
ORDER BY e.critical_events DESC;
