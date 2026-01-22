"""
generate_data.py

This script creates a small synthetic dataset that looks like "fleet operations logs":
- vehicles: which vehicle exists and where it operates
- routes: where it flies
- flights: each flight mission
- events: things that happened during a flight (GPS glitch, comms loss, etc.)
- maintenance: repairs after serious events

Why we do this:
You need reproducible data to practice SQL, dashboards, and data warehousing without
needing private/company data.
"""

from pathlib import Path
import numpy as np
import pandas as pd


# We use a random number generator with a fixed seed so results are repeatable.
# That means if you run the script today or tomorrow, you get the same dataset.
RNG = np.random.default_rng(seed=42)


def main(
    n_vehicles: int = 30,
    n_flights: int = 2000,
    start_date: str = "2025-09-01",
    days: int = 90,
) -> None:
    """
    Create synthetic CSVs inside:
      data/raw/   (raw logs)
      data/clean/ (cleaned logs - for now same as raw; we clean later)

    Parameters
    ----------
    n_vehicles: number of fleet vehicles
    n_flights: number of flights to simulate
    start_date: first possible date for flights
    days: how many days after start_date the flights can occur
    """

    # __file__ points to this script file. parents[2] jumps up to the repo root.
    repo_root = Path(__file__).resolve().parents[2]

    raw_dir = repo_root / "data" / "raw"
    clean_dir = repo_root / "data" / "clean"

    # Create folders if they don’t exist.
    raw_dir.mkdir(parents=True, exist_ok=True)
    clean_dir.mkdir(parents=True, exist_ok=True)

    # ----------------------------
    # 1) VEHICLES TABLE
    # ----------------------------
    vehicles = pd.DataFrame(
        {
            "vehicle_id": [f"V{str(i).zfill(3)}" for i in range(1, n_vehicles + 1)],
            "model": RNG.choice(["A", "B", "C"], size=n_vehicles, p=[0.4, 0.4, 0.2]),
            "region": RNG.choice(
                ["Kigali", "South", "East", "West", "North"], size=n_vehicles
            ),
            # Commission date = when the vehicle first started operating
            "commission_date": pd.to_datetime(start_date)
            - pd.to_timedelta(RNG.integers(30, 900, size=n_vehicles), unit="D"),
        }
    )

    # ----------------------------
    # 2) ROUTES TABLE
    # ----------------------------
    routes = pd.DataFrame(
        {
            "route_id": [f"R{str(i).zfill(3)}" for i in range(1, 26)],
            "route_name": [f"Route {i}" for i in range(1, 26)],
            "distance_km": RNG.integers(5, 120, size=25),
        }
    )

    # ----------------------------
    # 3) FLIGHTS TABLE
    # ----------------------------
    start_ts = pd.to_datetime(start_date)

    # Pick random start times for flights within [start_date, start_date + days]
    flight_start_times = start_ts + pd.to_timedelta(
        RNG.integers(0, days * 24 * 60, size=n_flights), unit="m"
    )

    # Random durations (minutes)
    durations_min = RNG.integers(8, 35, size=n_flights)

    flights = pd.DataFrame(
        {
            "flight_id": [f"F{str(i).zfill(6)}" for i in range(1, n_flights + 1)],
            "vehicle_id": RNG.choice(vehicles["vehicle_id"], size=n_flights),
            "route_id": RNG.choice(routes["route_id"], size=n_flights),
            "start_time": flight_start_times,
            "end_time": flight_start_times + pd.to_timedelta(durations_min, unit="m"),
            "planned_duration_min": durations_min + RNG.integers(-3, 4, size=n_flights),
        }
    )

    # Simple success/cancel simulation
    # success: 1 means success, 0 means failed
    flights["success"] = (RNG.random(n_flights) > 0.05).astype(int)  # ~95% success
    flights["cancelled"] = (RNG.random(n_flights) < 0.02).astype(int)  # ~2% cancelled

    # ----------------------------
    # 4) EVENTS TABLE
    # ----------------------------
    # Events happen during flights: e.g., GPS glitch, comms loss, etc.
    event_types = [
        "GPS_GLITCH",
        "BATTERY_DROP",
        "MOTOR_TEMP_HIGH",
        "COMMS_LOSS",
        "HARD_LANDING",
        "WIND_ALERT",
    ]
    severity_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    # Create a number of events proportional to flights
    n_events = int(n_flights * 0.9)

    # Choose which flight each event belongs to (some flights may have multiple events)
    chosen_flights = RNG.choice(flights["flight_id"], size=n_events, replace=True)

    events = pd.DataFrame(
        {
            "event_id": [f"E{str(i).zfill(7)}" for i in range(1, n_events + 1)],
            "flight_id": chosen_flights,
            "event_type": RNG.choice(
                event_types, size=n_events, p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.1]
            ),
            "severity": RNG.choice(
                severity_levels, size=n_events, p=[0.55, 0.25, 0.15, 0.05]
            ),
            "event_time": pd.NaT,  # we will fill this next
        }
    )

    # Put each event somewhere inside the flight time window
    flights_time = flights.set_index("flight_id")[["start_time", "end_time"]]
    starts = flights_time.loc[events["flight_id"], "start_time"].to_numpy()
    ends = flights_time.loc[events["flight_id"], "end_time"].to_numpy()

    # offsets are random numbers from 0..1 to pick a point between start and end
    offsets = RNG.random(n_events)
    events["event_time"] = pd.to_datetime(starts) + (
        pd.to_datetime(ends) - pd.to_datetime(starts)
    ) * offsets

    # ----------------------------
    # 5) MAINTENANCE TABLE
    # ----------------------------
    # Idea: HIGH/CRITICAL events more likely to cause maintenance work orders
    severe_flights = events.loc[
        events["severity"].isin(["HIGH", "CRITICAL"]), "flight_id"
    ].unique()

    maintenance_rows = []
    sample_size = min(120, len(severe_flights))

    # For some severe flights, create a maintenance record after the flight ends
    for fid in RNG.choice(severe_flights, size=sample_size, replace=False):
        vid = flights.loc[flights["flight_id"] == fid, "vehicle_id"].iloc[0]
        flight_end = flights.loc[flights["flight_id"] == fid, "end_time"].iloc[0]

        # maintenance happens between 1 hour and 7 days after the flight
        maint_time = flight_end + pd.to_timedelta(
            RNG.integers(60, 7 * 24 * 60), unit="m"
        )

        maintenance_rows.append(
            (
                f"WO_{fid}",  # work order id
                vid,
                maint_time,
                RNG.choice(["BATTERY", "MOTOR", "COMMS", "GPS", "AIRFRAME"]),
                1,  # resolved = 1 means fixed
            )
        )

    maintenance = pd.DataFrame(
        maintenance_rows,
        columns=["work_order_id", "vehicle_id", "timestamp", "issue_code", "resolved"],
    )

    # ----------------------------
    # SAVE TO CSV
    # ----------------------------
    # Save to raw and clean. Later we will transform raw -> clean in Snowflake/dbt.
    for df, name in [
        (vehicles, "vehicles"),
        (routes, "routes"),
        (flights, "flights"),
        (events, "events"),
        (maintenance, "maintenance"),
    ]:
        df.to_csv(raw_dir / f"{name}.csv", index=False)
        df.to_csv(clean_dir / f"{name}.csv", index=False)

    print("✅ Generated CSVs in data/raw and data/clean")


if __name__ == "__main__":
    # This makes the script runnable from the command line:
    # python python/src/generate_data.py
    main()
