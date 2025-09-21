from fastapi import APIRouter, HTTPException
from src.models.schema import QueryRequest, QueryResponse
from src.services.querytool import run_query

router = APIRouter(prefix="/pgsql", tags=["PostgreSQL"])

@router.post("/query", response_model=QueryResponse)
def query_tool(payload: QueryRequest):
    try:
        result = run_query(payload.sql, payload.skip, payload.take)
        return {
            "columns": result["columns"],
            "rows": result["rows"],
            "totalCount": result["totalCount"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
