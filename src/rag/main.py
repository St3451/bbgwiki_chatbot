import os
import nest_asyncio
from .llm_setup import init_llm
from .index_builder import build_index
from .query_engine import make_query_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def retrieve_and_query(
        query, 
        model="gpt-4o-mini", 
        temperature=1.0,
        docs_dir="bbgwiki/docs/", 
        top_k=2
        ):
    
    nest_asyncio.apply()

    # Initialize LLM (expects OPENAI_API_KEY in env)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")
    print("\nInitializing LLM...")
    init_llm(api_key, model, temperature)

    # Build index with context extractor
    print("Building index from documents...")
    index = build_index(docs_dir)

    # Create query engine
    print("Creating query engine...")
    query_engine = make_query_engine(
        index,
        top_k=top_k,
        mode="compact",
    )

    # Ask your question
    print("Executing query...")
    response = query_engine.query(query)

    return response
