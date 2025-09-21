import psycopg2
from psycopg2 import pool
import yaml
from pathlib import Path

# Load config
config_path = Path(__file__).resolve().parent.parent.parent / "env.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

db_conf = config["pgsql"]

# Buat connection pool global (minconn=1, maxconn=10 → bisa disesuaikan)
pg_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=db_conf["host"],
    port=db_conf["port"],
    database=db_conf["database"],
    user=db_conf["user"],
    password=db_conf["password"]
)

def run_query(sql: str, skip: int = 0, take: int = 100):
    # Safety check: hanya SELECT
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    conn = pg_pool.getconn()
    try:
        cur = conn.cursor()

        # --- Ambil total count ---
        count_sql = f"SELECT COUNT(*) FROM ({sql}) AS subquery"
        cur.execute(count_sql)
        total_count = cur.fetchone()[0]

        # --- Query dengan LIMIT/OFFSET ---
        query_with_limit = f"{sql} LIMIT {take} OFFSET {skip}"
        cur.execute(query_with_limit)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()

        result_rows = [dict(zip(columns, r)) for r in rows]

        return {
            "columns": columns,
            "rows": result_rows,
            "totalCount": total_count   # total real, bukan cuma len(rows)
        }

    except Exception as e:
        # kalau ada error, jangan balikin conn ke pool → close saja
        pg_pool.putconn(conn, close=True)
        raise e
    finally:
        # kalau berhasil, balikin conn ke pool
        if not conn.closed:
            pg_pool.putconn(conn)
