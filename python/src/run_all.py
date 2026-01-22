"""
run_all.py

One-command pipeline:
1) Generate simulated fleet data (CSV files)
2) Run SQL metrics in DuckDB
3) Produce the final output used by Power BI:
   data/outputs/weekly_metrics.csv

Run:
    python python/src/run_all.py
"""

import subprocess
import sys
from pathlib import Path


def run_step(step_name: str, command: list[str], repo_root: Path) -> None:
    """Run a subprocess command and stop immediately if it fails."""
    print(f"\n=== {step_name} ===")
    result = subprocess.run(command, cwd=repo_root, text=True)
    if result.returncode != 0:
        raise SystemExit(f"Step failed: {step_name}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    # Step 1: Generate synthetic raw/clean CSVs
    run_step(
        "Generate simulated data",
        [sys.executable, "python/src/generate_data.py"],
        repo_root,
    )

    # Step 2: Run SQL aggregation to produce weekly_metrics.csv
    run_step(
        "Compute weekly monitoring metrics",
        [sys.executable, "python/src/run_sql_duckdb.py"],
        repo_root,
    )

    print("\n✅ Pipeline complete!")
    print("Output file: data/outputs/weekly_metrics.csv")


if __name__ == "__main__":
    main()
