from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.graph.workflow import build_trading_pipeline

app = FastAPI()

# Allow React to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the graph globally
agent_app = build_trading_pipeline()
thread_config = {"configurable": {"thread_id": "react_dashboard_session"}}

@app.post("/start")
async def start_workflow():
    initial_state = {
        "watchlist": ["AAPL", "NVDA", "PLTR"],
        "human_approved": False
    }
    
    # Run the graph until it hits the interrupt_before breakpoint
    async for event in agent_app.astream(initial_state, thread_config, stream_mode="values"):
        pass 
        
    # Fetch the paused state to send to React
    current_state = agent_app.get_state(thread_config).values
    
    return {
        "news_summary": current_state.get("news_summary", ""),
        "audit_log": current_state.get("audit_log", []),
        "validated_orders": current_state.get("validated_orders", [])
    }

class ApprovalRequest(BaseModel):
    approved: bool

@app.post("/approve")
async def handle_approval(request: ApprovalRequest):
    if request.approved:
        agent_app.update_state(thread_config, {"human_approved": True})
        # Resume graph execution
        async for event in agent_app.astream(None, thread_config, stream_mode="values"):
            pass
        return {"message": "Trades executed successfully via Alpaca!"}
    else:
        return {"message": "Trades rejected. Graph terminated."}