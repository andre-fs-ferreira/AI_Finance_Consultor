from src.llm.llm_client import get_llm
from src.graph.state import FundState

async def analyst_node(state: FundState):
    llm = get_llm()
    
    prompt = f"""
    You are an expert financial analyst. Review today's news for our watchlist:
    {state['daily_news']}
    
    Provide a concise daily digest ("resume findings") highlighting key positive/negative 
    catalysts for each stock. Do not suggest trades yet.
    """
    
    response = await llm.ainvoke(prompt)
    return {"news_summary": response.content} # Updates the state graph