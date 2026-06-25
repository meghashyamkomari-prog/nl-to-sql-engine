from fastapi import APIRouter, HTTPException
from schemas.models import NLQuery, QueryResult
from services.nl_to_sql import generate_sql, explain_results
from services.executor import execute_sql

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/ask", response_model=QueryResult)
async def ask_question(query: NLQuery):
    try:
        sql = generate_sql(query.question)
        results = execute_sql(sql)
        explanation = explain_results(query.question, sql, results)
        return QueryResult(
            question=query.question,
            generated_sql=sql,
            results=results[:100],
            row_count=len(results),
            ai_explanation=explanation
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "NL to SQL Engine"}
