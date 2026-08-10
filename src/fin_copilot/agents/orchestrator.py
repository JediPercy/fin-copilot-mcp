import json
import anthropic
from fin_copilot.core.config import settings
from fin_copilot.core.logging import logger
from fin_copilot.mcp_servers.sql_server import validate_sql, execute_query, get_schema
from fin_copilot.mcp_servers.stripe_server import get_mrr_metrics, list_recent_disputes
from fin_copilot.mcp_servers.market_server import get_stock_price, get_historical_volatility
from fin_copilot.agents.prompts import ORCHESTRATOR_SYSTEM_PROMPT
from fin_copilot.agents.validator import validate_financial_output

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY.get_secret_value())

TOOLS = [
    {
        "name": "validate_sql",
        "description": "Validates SQL query syntax using PostgreSQL EXPLAIN before execution.",
        "input_schema": {
            "type": "object",
            "properties": {"sql_query": {"type": "string"}},
            "required": ["sql_query"],
        },
    },
    {
        "name": "execute_query",
        "description": "Executes a validated read-only SQL query against PostgreSQL.",
        "input_schema": {
            "type": "object",
            "properties": {"sql_query": {"type": "string"}},
            "required": ["sql_query"],
        },
    },
    {
        "name": "get_mrr_metrics",
        "description": "Retrieves Monthly Recurring Revenue (MRR) and Net Revenue Retention metrics.",
        "input_schema": {
            "type": "object",
            "properties": {"period": {"type": "string"}},
            "required": ["period"],
        },
    },
    {
        "name": "get_stock_price",
        "description": "Fetches equity prices and ticker metrics from Yahoo Finance.",
        "input_schema": {
            "type": "object",
            "properties": {"ticker": {"type": "string"}},
            "required": ["ticker"],
        },
    },
]


def run_query_with_self_healing(
    user_query: str, max_retries: int = settings.MAX_HEALING_RETRIES
) -> str:
    schema_context = get_schema()
    system_prompt = ORCHESTRATOR_SYSTEM_PROMPT.format(schema_context=schema_context)
    messages = [{"role": "user", "content": user_query}]

    for attempt in range(max_retries):
        logger.info("Orchestrator Execution Step", attempt=attempt + 1)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            tools=TOOLS,
            messages=messages,
        )

        tool_uses = [c for c in response.content if c.type == "tool_use"]
        if not tool_uses:
            return response.content[0].text

        tool_results = []
        for tool_use in tool_uses:
            tool_name = tool_use.name
            args = tool_use.input
            logger.info("Executing MCP Tool Call", tool_name=tool_name, args=args)

            if tool_name == "validate_sql":
                result = validate_sql(args["sql_query"])
            elif tool_name == "execute_query":
                result = execute_query(args["sql_query"])
                val_check = validate_financial_output(result)
                result["financial_validation"] = val_check
            elif tool_name == "get_mrr_metrics":
                result = get_mrr_metrics(args.get("period", "current"))
            elif tool_name == "get_stock_price":
                result = get_stock_price(args["ticker"])
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result),
                }
            )

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return "Execution halted: Exceeded maximum self-healing retries."


if __name__ == "__main__":
    query = "Check our MRR metrics and compare with S&P 500 (^GSPC) price."
    print(run_query_with_self_healing(query))