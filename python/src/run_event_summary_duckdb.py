"""
run_event_summary_duckdb.py

Runs sql/event_type_summary.sql in DuckDB and saves:
data/outputs/event_type_summary.csv
"""

from pathlib import Path
import duckdb


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    sql_path = repo_root / "sql" / "event_type_summary.sql"
    out_dir = repo_root / "data" / "outputs"
    out_path = out_dir / "event_type_summary.csv"

    out_dir.mkdir(parents=True, exist_ok=True)

    query = sql_path.read_text(encoding="utf-8")
    con = duckdb.connect()
    df = con.execute(query).df()
    df.to_csv(out_path, index=False)

    print(f"✅ Saved: {out_path}")


if __name__ == "__main__":
    main()
