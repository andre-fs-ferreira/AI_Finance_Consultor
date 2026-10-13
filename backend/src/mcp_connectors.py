from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_trading_tools():
    client = MultiServerMCPClient({
        # Server 1: Fetching Market Data & News
        "finance": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["finance-mcp-server"] # Open-source Yahoo Finance MCP
        },
        # Server 2: Official Alpaca Paper Trading execution
        "alpaca": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["alpaca-mcp-server"],
            "env": {
                "ALPACA_API_KEY": "YOUR_PAPER_KEY",
                "ALPACA_SECRET_KEY": "YOUR_PAPER_SECRET",
                "ALPACA_PAPER_TRADE": "true"
            }
        }
    })
    return await client.get_tools()