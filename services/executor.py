import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def execute_sql(sql: str) -> list:
    engine = create_engine(os.getenv("DATABASE_URL"))
    forbidden = ["drop", "delete", "update", "insert", "alter", "truncate"]
    sql_lower = sql.lower()
    for word in forbidden:
        if word in sql_lower:
            raise ValueError(f"Forbidden SQL operation: {word}")
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
