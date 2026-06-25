from pydantic import BaseModel
from typing import Optional, List, Any

class NLQuery(BaseModel):
    question: str
    database: Optional[str] = "financial_db"

class QueryResult(BaseModel):
    question: str
    generated_sql: str
    results: List[Any]
    row_count: int
    ai_explanation: Optional[str] = None

class QueryHistory(BaseModel):
    id: int
    question: str
    generated_sql: str
    row_count: int
