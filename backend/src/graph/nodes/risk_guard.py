from src.graph.state import FundState
from src.skills.risk_guard import validate_and_clamp_order

async def risk_guard_node(state: FundState):
    proposals = state.get("trade_proposals", [])
    holdings = state.get("current_holdings", {})
    cash = state.get("portfolio_balance", 0.0)
    total_value = state.get("total_portfolio_value", cash)
    
    validated = []
    logs = []
    daily_spent = 0.0

    for proposal in proposals:
        ticker = proposal["ticker"]
        # Fetch current price from holdings or market data snapshot
        current_price = holdings.get(ticker, {}).get("current_price", 100.0)
        current_ticker_val = holdings.get(ticker, {}).get("market_value", 0.0)

        result = validate_and_clamp_order(
            proposal=proposal,
            current_price=current_price,
            cash_available=cash,
            total_portfolio_value=total_value,
            current_ticker_value=current_ticker_val,
            daily_spent_so_far=daily_spent
        )

        if result["status"] == "APPROVED" and result["shares_to_execute"] > 0:
            validated.append(result)
            cost = result.get("estimated_cost", 0.0)
            daily_spent += cost
            cash -= cost
            logs.append(f"✅ Approved: {result['action']} {result['shares_to_execute']} shares of {ticker}")
        else:
            logs.append(f"⛔ Blocked/Filtered: {ticker} - {result.get('reason', 'Hold or zero shares')}")

    return {
        "validated_orders": validated,
        "audit_log": logs
    }