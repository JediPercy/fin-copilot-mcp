from fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("Market Telemetry Server")


@mcp.tool()
def get_stock_price(ticker: str) -> dict:
    """Fetches current equity price and daily change for a ticker (e.g. AAPL, MSFT, ^GSPC)."""
    try:
        stock = yf.Ticker(ticker)
        fast_info = stock.fast_info
        return {
            "ticker": ticker.upper(),
            "last_price": round(float(fast_info.last_price), 2),
            "previous_close": round(float(fast_info.previous_close), 2),
            "currency": fast_info.currency,
        }
    except Exception as e:
        return {"error": f"Failed to fetch market data for {ticker}: {str(e)}"}


@mcp.tool()
def get_historical_volatility(ticker: str, period: str = "1mo") -> dict:
    """Calculates historical volatility for a given ticker over a period (1mo, 3mo, 1y)."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if hist.empty:
            return {"error": f"No data found for {ticker}"}
        returns = hist["Close"].pct_change().dropna()
        volatility = returns.std() * (252**0.5)  # Annualized volatility
        return {
            "ticker": ticker.upper(),
            "period": period,
            "annualized_volatility": round(float(volatility), 4),
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()