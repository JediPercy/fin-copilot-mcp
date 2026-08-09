import json
from fastmcp import FastMCP

mcp = FastMCP("Stripe Financial Server")

MOCK_STRIPE_DATA = {
    "mrr": 145000.00,
    "arr": 1740000.00,
    "net_revenue_retention": 1.12,
    "active_customers": 580,
    "churn_rate_monthly": 0.018,
}


@mcp.resource("stripe://summary")
def get_stripe_summary() -> str:
    """Returns high-level subscription metrics."""
    return json.dumps(MOCK_STRIPE_DATA, indent=2)


@mcp.tool()
def get_mrr_metrics(period: str = "current") -> dict:
    """Retrieves Monthly Recurring Revenue (MRR) and Net Revenue Retention (NRR)."""
    return {
        "period": period,
        "mrr_usd": MOCK_STRIPE_DATA["mrr"],
        "nrr": MOCK_STRIPE_DATA["net_revenue_retention"],
        "churn_rate": MOCK_STRIPE_DATA["churn_rate_monthly"],
    }


@mcp.tool()
def list_recent_disputes(limit: int = 5) -> list[dict]:
    """Retrieves recent billing disputes and chargebacks."""
    return [
        {"id": "dp_201", "amount": 1200.00, "status": "needs_response", "reason": "fraudulent"},
        {"id": "dp_202", "amount": 450.00, "status": "won", "reason": "subscription_canceled"},
    ][:limit]


if __name__ == "__main__":
    mcp.run()