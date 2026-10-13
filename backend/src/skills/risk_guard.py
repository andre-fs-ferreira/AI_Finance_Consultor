from src.config import CONFIG
from typing import Dict, List, Any

class RiskViolationError(Exception):
    pass

def validate_and_clamp_order(
    proposal: Dict[str, Any],
    current_price: float,
    cash_available: float,
    total_portfolio_value: float,
    current_ticker_value: float,
    daily_spent_so_far: float
) -> Dict[str, Any]:
    ticker = proposal["ticker"]
    action = proposal["action"].upper()
    requested_amount = proposal.get("amount", 0) # number of shares

    if action == "HOLD":
        return {**proposal, "status": "APPROVED", "shares_to_execute": 0}

    if action not in CONFIG.allowed_actions:
        return {**proposal, "status": "REJECTED", "reason": f"Disallowed action: {action}"}

    # Handle SELL
    if action == "SELL":
        # Ensure we do not sell more shares than we own
        shares_owned = current_ticker_value / current_price if current_price > 0 else 0
        executable_shares = min(requested_amount, int(shares_owned))
        if executable_shares <= 0:
            return {**proposal, "status": "REJECTED", "reason": "No shares available to sell"}
        return {**proposal, "status": "APPROVED", "shares_to_execute": executable_shares}

    # Handle BUY
    if action == "BUY":
        order_cost = requested_amount * current_price

        # Check 1: Individual Order Size Limit
        if order_cost > CONFIG.max_order_value_usd:
            # Clamp shares down to fit max allowed order value
            requested_amount = int(CONFIG.max_order_value_usd // current_price)
            order_cost = requested_amount * current_price

        if requested_amount <= 0:
            return {**proposal, "status": "REJECTED", "reason": f"Share price (${current_price:.2f}) exceeds max single order limit (${CONFIG.max_order_value_usd})"}

        # Check 2: Daily Budget Cap
        if (daily_spent_so_far + order_cost) > CONFIG.max_daily_budget_usd:
            remaining_budget = CONFIG.max_daily_budget_usd - daily_spent_so_far
            requested_amount = int(remaining_budget // current_price)
            order_cost = requested_amount * current_price

        if requested_amount <= 0:
            return {**proposal, "status": "REJECTED", "reason": "Daily budget cap reached"}

        # Check 3: Cash Floor Protection
        if (cash_available - order_cost) < CONFIG.min_cash_reserve_usd:
            max_spendable_cash = max(0.0, cash_available - CONFIG.min_cash_reserve_usd)
            requested_amount = int(max_spendable_cash // current_price)
            order_cost = requested_amount * current_price

        if requested_amount <= 0:
            return {**proposal, "status": "REJECTED", "reason": "Trade violates minimum cash reserve floor"}

        # Check 4: Portfolio Allocation Limit
        projected_ticker_value = current_ticker_value + order_cost
        max_allowed_ticker_value = total_portfolio_value * CONFIG.max_portfolio_allocation_pct
        if projected_ticker_value > max_allowed_ticker_value:
            allowed_expansion = max(0.0, max_allowed_ticker_value - current_ticker_value)
            requested_amount = int(allowed_expansion // current_price)

        if requested_amount <= 0:
            return {**proposal, "status": "REJECTED", "reason": f"Would exceed {CONFIG.max_portfolio_allocation_pct*100}% allocation limit for {ticker}"}

        return {
            **proposal,
            "status": "APPROVED",
            "shares_to_execute": requested_amount,
            "estimated_cost": requested_amount * current_price
        }