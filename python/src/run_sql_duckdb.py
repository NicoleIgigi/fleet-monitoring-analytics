"""
run_sql_duckdb.py

This script:
1) Reads sql/metrics.sql
2) Executes it using DuckDB (a tiny local SQL engine)
3) Saves the result as data/outputs/weekly_metrics.csv

Why this is useful:
- You can re-run it anytime after updating SQL
- Power BI can load the output CSV immediately
"""

from pathlib import Path
import duckdb


def main() -> None:
    # Find the repo root folder
    repo_root = Path(__file__).resolve().parents[2]

    # Paths to the SQL query and the output CSV
    sql_path = repo_root / "sql" / "metrics.sql"
    out_dir = repo_root / "data" / "outputs"
    out_path = out_dir / "weekly_metrics.csv"

    # Ensure output directory exists
    out_dir.mkdir(parents=True, exist_ok=True)

    # Read the SQL text from file
    query = sql_path.read_text(encoding="utf-8")

    # Connect to DuckDB (in-memory by default)
    con = duckdb.connect()

    # Execute query and return results as a pandas DataFrame
    df = con.execute(query).df()

    # Save results for Power BI / inspection
    df.to_csv(out_path, index=False)

    print(f"✅ Saved metrics to: {out_path}")


if __name__ == "__main__":
    main()
