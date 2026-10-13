from src.graph.state import FundState

async def executor_node(state: FundState):
    orders = state.get("validated_orders", [])
    
    if not orders:
        print("ℹ️ Executor: No approved orders to execute today.")
        return {}

    for order in orders:
        ticker = order["ticker"]
        action = order["action"].upper()
        shares = order["shares_to_execute"]
        
        print(f"🚀 Executing Trade: {action} {shares} shares of {ticker}")
        # Note: This is where the Alpaca MCP tool call goes when you plug in your API!

    return {}