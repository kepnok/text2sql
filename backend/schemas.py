from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    sql: str
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
