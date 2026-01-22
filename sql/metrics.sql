-- metrics.sql
-- We use DuckDB to query CSV files directly.
-- This lets us practice "warehouse-style" SQL with window functions without installing a database.

WITH flights AS (
  SELECT * FROM read_csv_auto('data/clean/flights.csv')
),
vehicles AS (
  SELECT * FROM read_csv_auto('data/clean/vehicles.csv')
),
events AS (
  SELECT * FROM read_csv_auto('data/clean/events.csv')
),

-- Combine flights + vehicle info so every flight has region/model
flight_base AS (
  SELECT
    f.flight_id,
    f.vehicle_id,
    v.model,
    v.region,
    CAST(f.start_time AS TIMESTAMP) AS start_time,
    CAST(f.end_time AS TIMESTAMP) AS end_time,
    CAST(f.success AS INTEGER) AS success,
    CAST(f.cancelled AS INTEGER) AS cancelled,
    date_trunc('week', CAST(f.start_time AS TIMESTAMP)) AS week
  FROM flights f
  JOIN vehicles v
    ON f.vehicle_id = v.vehicle_id
),

-- Count how many HIGH/CRITICAL events happened per flight
critical_events_per_flight AS (
  SELECT
    e.flight_id,
    COUNT(*) AS critical_event_count
  FROM events e
  WHERE e.severity IN ('HIGH','CRITICAL')
  GROUP BY e.flight_id
),

-- Aggregate to weekly metrics (this is what leaders/engineers track)
weekly_metrics AS (
  SELECT
    b.week,
    b.region,
    b.model,
    COUNT(*) AS flights_total,
    SUM(b.success) AS flights_success,
    SUM(b.cancelled) AS flights_cancelled,
    SUM(COALESCE(c.critical_event_count, 0)) AS critical_events
  FROM flight_base b
  LEFT JOIN critical_events_per_flight c
    ON b.flight_id = c.flight_id
  GROUP BY 1,2,3
),

-- Add "rates" + week-over-week change using a window function
final AS (
  SELECT
    week,
    region,
    model,
    flights_total,
    flights_success,

    -- Reliability % = success / total flights
    ROUND(100.0 * flights_success / NULLIF(flights_total, 0), 2) AS reliability_pct,

    -- Critical events per 100 flights = (critical_events / flights_total) * 100
    ROUND(100.0 * critical_events / NULLIF(flights_total, 0), 2) AS critical_events_per_100_flights,

    -- Week-over-week change in reliability (window function)
    ROUND(
      (ROUND(100.0 * flights_success / NULLIF(flights_total, 0), 2)
       - LAG(ROUND(100.0 * flights_success / NULLIF(flights_total, 0), 2))
         OVER (PARTITION BY region, model ORDER BY week)
      ),
      2
    ) AS reliability_wow_change
  FROM weekly_metrics
)

SELECT *
FROM final
ORDER BY week, region, model;
