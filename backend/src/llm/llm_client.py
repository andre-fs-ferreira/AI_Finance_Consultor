from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        base_url="http://localhost:11434/v1",  # Keeps pointing to Mac-native Ollama
        api_key="ollama",                      
        model="gemma4:e2b",                    # Swapped to the small Gemma model
        temperature=0.1                        # Keep temperature low for strict JSON adherence
    )