import json
from src.llm.llm_client import get_llm
from src.graph.state import FundState

async def strategist_node(state: FundState):
    llm = get_llm() 
    
    prompt = f"""
    Given the current portfolio: {state['current_holdings']}
    And today's news digest: {state['news_summary']}
    
    Decide whether to BUY, SELL, or HOLD each stock in the watchlist.
    Return ONLY a raw JSON array of objects with keys: "ticker", "action", "amount", "reasoning".
    """
    
    response = await llm.ainvoke(prompt)
    
    try:
        # Clean up the output in case the LLM wraps it in markdown blocks
        content = response.content.replace("```json", "").replace("```", "").strip()
        proposals = json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Strategist failed to output valid JSON. Defaulting to HOLD.")
        proposals = []
        
    return {"trade_proposals": proposals}