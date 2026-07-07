import ollama
from sqlalchemy import inspect
from database import engine

MODEL_NAME = "qwen2.5:3b"

def get_database_schema():
    inspector = inspect(engine)
    schema = []
    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append(f"{column['name']} ({column['type']})")
        schema.append(f"Table: {table_name}\nColumns: {', '.join(columns)}")
    return "\n\n".join(schema)

def generate_sql(query: str) -> str:
    schema_info = get_database_schema()
    
    prompt = f"""You are a PostgreSQL expert. Given the following database schema, write a SQL query to answer the user's question. 
Return ONLY the raw SQL query, without any markdown formatting, explanation, or code blocks. Do not wrap in ```sql.

Schema:
{schema_info}

Question: {query}

SQL Query:"""

    try:
        response = ollama.generate(model=MODEL_NAME, prompt=prompt)
        sql = response['response'].strip()
        
        # Clean up in case the model returns markdown blocks anyway
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
            
        return sql.strip()
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ""
