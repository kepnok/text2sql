from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import llm
from database import get_db, engine
from schemas import QueryRequest, QueryResponse
from typing import Dict, Any, List

app = FastAPI(title="Text-to-SQL API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/schema")
def get_schema():
    """Returns the current database schema as a string."""
    try:
        return {"schema": llm.get_database_schema()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-sql", response_model=QueryResponse)
def generate_and_execute_sql(request: QueryRequest, db: Session = Depends(get_db)):
    """Generates SQL from natural language and executes it."""
    try:
        # 1. Generate SQL
        sql_query = llm.generate_sql(request.query)
        if not sql_query:
            return QueryResponse(sql="", error="Failed to generate SQL from the LLM.")
        
        # 2. Execute SQL
        # Safety check - simple prevention of destructive queries (not foolproof, but good for demo)
        upper_sql = sql_query.upper()
        if any(keyword in upper_sql for keyword in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]):
             return QueryResponse(sql=sql_query, error="Only SELECT queries are allowed for safety.")

        result = db.execute(text(sql_query))
        
        # Fetch rows
        rows = result.fetchall()
        # Get column names
        columns = result.keys()
        
        # Convert to list of dicts
        results_list = [dict(zip(columns, row)) for row in rows]
        
        return QueryResponse(sql=sql_query, results=results_list)
        
    except Exception as e:
        # If execution fails, return the generated SQL and the error
        return QueryResponse(sql=sql_query if 'sql_query' in locals() else "", error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
