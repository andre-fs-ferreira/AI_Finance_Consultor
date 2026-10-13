from src.graph.state import FundState

async def researcher_node(state: FundState):
    print("🔍 Market Researcher: Fetching news for watchlist...")
    
    # Mocking the data that the MCP server would normally return
    mock_news = {
        "AAPL": "Apple announces groundbreaking new AI chip. Analysts expect strong revenue growth.",
        "NVDA": "Nvidia faces slight supply chain delays, but demand remains at an all-time high.",
        "PLTR": "Palantir secures a massive new government contract for defense AI."
    }
    
    # Mock portfolio setup
    mock_holdings = {
        "AAPL": {"shares": 2, "current_price": 150.0, "market_value": 300.0}
    }
    
    return {
        "daily_news": mock_news,
        "current_holdings": mock_holdings,
        "portfolio_balance": 10000.0,
        "total_portfolio_value": 10300.0
    }