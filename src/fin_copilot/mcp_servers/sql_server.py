import json
from fastmcp import FastMCP
from sqlalchemy import create_engine, text, inspect
from fin_copilot.core.config import settings
from fin_copilot.core.logging import logger

mcp = FastMCP("SQL Engine Server")


def get_db_engine():
    """Creates SQLAlchemy connection engine targeting PostgreSQL (e.g. Neon.tech)."""
    return create_engine(settings.DATABASE_URL, pool_pre_ping=True)


@mcp.resource("schema://database")
def get_schema() -> str:
    """Inspects PostgreSQL database schema using SQLAlchemy."""
    engine = get_db_engine()
    try:
        inspector = inspect(engine)
        schema_info = []
        tables = inspector.get_table_names()
        for table in tables:
            columns = inspector.get_columns(table)
            col_defs = [f"  - {col['name']} ({col['type']})" for col in columns]
            schema_info.append(f"Table '{table}':\n" + "\n".join(col_defs))
        return "\n\n".join(schema_info) if schema_info else "No tables found in database."
    except Exception as e:
        logger.error("Failed to inspect database schema", error=str(e))
        return f"Error reading schema: {str(e)}"


@mcp.tool()
def validate_sql(sql_query: str) -> dict:
    """Dry-runs SQL via PostgreSQL EXPLAIN to verify syntax and column existence."""
    if not sql_query.strip().upper().startswith("SELECT"):
        return {"valid": False, "error": "Only read-only SELECT queries are allowed."}

    engine = get_db_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text(f"EXPLAIN {sql_query}"))
        return {"valid": True, "error": None}
    except Exception as e:
        return {"valid": False, "error": str(e)}


@mcp.tool()
def execute_query(sql_query: str) -> dict:
    """Executes a validated read-only SQL query against PostgreSQL."""
    validation = validate_sql(sql_query)
    if not validation["valid"]:
        return {"success": False, "error": f"Validation failed: {validation['error']}"}

    engine = get_db_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            columns = list(result.keys())
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            return {"success": True, "columns": columns, "data": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    mcp.run()