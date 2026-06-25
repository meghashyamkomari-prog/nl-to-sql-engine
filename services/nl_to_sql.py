import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SCHEMA_CONTEXT = """
Database: financial_db (PostgreSQL)
Tables:
1. raw_stock_prices: ingested_at, open, high, low, close, volume, dividends, stock_splits, date, symbol
2. llm_classified_transactions: transaction details with AI classifications
3. healthcare_by_state: healthcare data by US state
4. healthcare_by_specialty: healthcare data by medical specialty

Rules:
- Always use lowercase table names
- Use date column for filtering by date
- Use symbol column for stock filtering (AAPL, MSFT, GOOGL, JPM, BAC)
- Return only valid PostgreSQL SQL
- Never use DROP, DELETE, UPDATE, INSERT
- Only SELECT statements allowed
"""

def generate_sql(question: str) -> str:
    prompt = f"""
You are a SQL expert. Convert this natural language question to PostgreSQL SQL.

{SCHEMA_CONTEXT}

Question: {question}

Rules:
- Return ONLY the SQL query
- No explanations
- No markdown
- No backticks
- Just the raw SQL query ending with semicolon
"""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    sql = message.content[0].text.strip()
    if sql.startswith("```"):
        sql = sql.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return sql

def explain_results(question: str, sql: str, results: list) -> str:
    if not results:
        return "No results found for your query."
    prompt = f"""
Question: {question}
SQL: {sql}
Results (first 5 rows): {results[:5]}

Provide a brief 2-3 sentence explanation of the results in plain English.
"""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()
