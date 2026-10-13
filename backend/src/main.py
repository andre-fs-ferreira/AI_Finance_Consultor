import asyncio
from src.graph.workflow import build_trading_pipeline

async def main():
    app = build_trading_pipeline()
    
    # Setup initial state for today's run
    thread_config = {"configurable": {"thread_id": "daily_run_test_1"}}
    initial_state = {
        "watchlist": ["AAPL", "NVDA", "PLTR"],
        "human_approved": False
    }
    
    print("🚀 Starting Daily AI Trader Analysis...")
    
    # 1. Run the graph until it hits the interrupt_before breakpoint
    async for event in app.astream(initial_state, thread_config, stream_mode="values"):
        if "news_summary" in event:
            print("\n📰 TODAY's FINDINGS:\n", event["news_summary"])
        if "audit_log" in event and event["audit_log"]:
            print("\n🛡️ RISK GUARD LOG:")
            for log in event["audit_log"]:
                print(log)
            
    # 2. Fetch the state where it paused
    current_state = app.get_state(thread_config).values
    validated_orders = current_state.get("validated_orders", [])
    
    if not validated_orders:
        print("\n🛑 No valid orders passed the Risk Guard. Exiting.")
        return

    print("\n⚖️ VALIDATED TRADES READY FOR EXECUTION:")
    for trade in validated_orders:
        print(f"[{trade['action']}] {trade['shares_to_execute']} shares of {trade['ticker']} (Est Cost: ${trade.get('estimated_cost', 0):.2f})")
        
    # 3. MODERATOR APPROVAL
    user_input = input("\nDo you approve these trades for Alpaca execution? (yes/no): ")
    
    if user_input.lower() == 'yes':
        print("\n✅ Trades approved. Resuming Execution...")
        app.update_state(thread_config, {"human_approved": True})
        
        # Resume graph to trigger the Trade_Executor node
        async for event in app.astream(None, thread_config, stream_mode="values"):
            pass 
        print("🎉 Execution Complete!")
    else:
        print("\n❌ Trades denied. Graph terminated.")

if __name__ == "__main__":
    asyncio.run(main())