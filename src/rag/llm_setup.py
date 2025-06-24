from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

def init_llm(
    api_key: str,
    model: str = "gpt-4o-mini",
    temperature: float = 1.0
):
    """
    Initialize and register the LLM in llama_index.Settings,
    with custom OpenAI parameters.
    """
    llm = OpenAI(
        model=model,
        api_key=api_key,
        temperature=temperature,
    )
    Settings.llm = llm
    return llm
