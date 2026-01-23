"""
validate_outputs.py

Basic data quality checks for generated outputs.
These checks simulate "system health monitoring best practices":
- required columns exist
- no negative values
- reliability in valid range (0–100)
- critical events per 100 flights non-negative
"""

from pathlib import Path
import pandas as pd


def fail(msg: str) -> None:
    raise SystemExit(f"❌ Data quality check failed: {msg}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    weekly_path = repo_root / "data" / "outputs" / "weekly_metrics.csv"
    drivers_path = repo_root / "data" / "outputs" / "event_type_summary.csv"

    if not weekly_path.exists():
        fail(f"Missing file: {weekly_path}")
    if not drivers_path.exists():
        fail(f"Missing file: {drivers_path}")

    weekly = pd.read_csv(weekly_path)
    drivers = pd.read_csv(drivers_path)

    # ---- weekly_metrics checks ----
    required_weekly = {
        "week",
        "region",
        "model",
        "flights_total",
        "flights_success",
        "reliability_pct",
        "critical_events_per_100_flights",
    }
    missing = required_weekly - set(weekly.columns)
    if missing:
        fail(f"weekly_metrics.csv missing columns: {sorted(missing)}")

    if (weekly["flights_total"] < 0).any():
        fail("weekly_metrics.csv has negative flights_total")
    if (weekly["flights_success"] < 0).any():
        fail("weekly_metrics.csv has negative flights_success")
    if (weekly["flights_success"] > weekly["flights_total"]).any():
        fail("weekly_metrics.csv has flights_success > flights_total")

    # reliability_pct should be in 0–100
    if ((weekly["reliability_pct"] < 0) | (weekly["reliability_pct"] > 100)).any():
        fail("weekly_metrics.csv has reliability_pct outside 0–100")

    if (weekly["critical_events_per_100_flights"] < 0).any():
        fail("weekly_metrics.csv has negative critical_events_per_100_flights")

    # ---- event_type_summary checks ----
    required_drivers = {"event_type", "total_events", "critical_events"}
    missing2 = required_drivers - set(drivers.columns)
    if missing2:
        fail(f"event_type_summary.csv missing columns: {sorted(missing2)}")

    if (drivers["total_events"] < 0).any():
        fail("event_type_summary.csv has negative total_events")
    if (drivers["critical_events"] < 0).any():
        fail("event_type_summary.csv has negative critical_events")
    if (drivers["critical_events"] > drivers["total_events"]).any():
        fail("event_type_summary.csv has critical_events > total_events")

    print("✅ Data quality checks passed!")


if __name__ == "__main__":
    main()
