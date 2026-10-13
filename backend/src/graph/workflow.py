from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.graph.state import FundState
from src.graph.nodes import (
    researcher_node,
    analyst_node,
    strategist_node,
    risk_guard_node,
    executor_node
)

def build_trading_pipeline():
    builder = StateGraph(FundState)

    # 1. Add all 5 nodes
    builder.add_node("Market_Researcher", researcher_node)
    builder.add_node("News_Analyst", analyst_node)
    builder.add_node("Strategist", strategist_node)
    builder.add_node("Risk_Guard", risk_guard_node)
    builder.add_node("Trade_Executor", executor_node)

    # 2. Define the exact sequential flow
    builder.add_edge(START, "Market_Researcher")
    builder.add_edge("Market_Researcher", "News_Analyst")
    builder.add_edge("News_Analyst", "Strategist")
    builder.add_edge("Strategist", "Risk_Guard")
    builder.add_edge("Risk_Guard", "Trade_Executor")
    builder.add_edge("Trade_Executor", END)

    # 3. Add the memory checkpointer to allow pausing before execution
    memory = MemorySaver()
    
    return builder.compile(
        checkpointer=memory,
        interrupt_before=["Trade_Executor"] 
    )