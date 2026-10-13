from pydantic import BaseModel

class RiskSettings(BaseModel):
    # Capital Limits
    max_order_value_usd: float = 500.0        # Max dollars allowed for a single order
    max_daily_budget_usd: float = 2000.0      # Max total dollars deployed across all trades in a day
    min_cash_reserve_usd: float = 1000.0      # Untouchable cash cushion in your account

    # Concentration Limits
    max_portfolio_allocation_pct: float = 0.15  # Max 15% of total portfolio in any single ticker
    allowed_actions: list[str] = ["BUY", "SELL", "HOLD"]

CONFIG = RiskSettings()
WATCHLIST = ["AAPL", "NVDA", "MSFT", "AMZN"]