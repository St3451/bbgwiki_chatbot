import os
import nest_asyncio
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import Settings
from .llm_setup import init_llm
from .index_builder import build_index
from .query_engine import make_query_engine
from .utils import load_yaml

# Load environment variables from .env
load_dotenv()

PERSIST_DIR = "vectore_store/"
EMBED_MODEL = "baai/bge-small-en-v1.5"
PROMPT_YAML = "config/prompts.yaml"

Settings.embed_model = HuggingFaceEmbedding(
    model_name=EMBED_MODEL
)

def build_and_query(
    query: str,
    model: str = "gpt-4o-mini",
    temperature: float = 1.0,
    prompt_template_mode: str = "compact",
    docs_dir: str = "bbgwiki/docs/",
    top_k: int = 2,
    force_rebuild: bool = False,
    doc_ext: list[str] = [".md"]
):
    """
    Builds the index, retrieves context, and queries the LLM.
    - If force_rebuild=True or no persisted index exists, builds & persists the index.
    - Otherwise loads the existing index.
    - Then runs `query` against it and returns the response.
    """

    custom_prompts = load_yaml(PROMPT_YAML)

    # Patch asyncio to allow nested event loops
    nest_asyncio.apply()

    # Initialize LLM (expects OPENAI_API_KEY in env)
    print("\nInitializing LLM...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")
    init_llm(api_key, model, temperature)

    # Decide whether to build or load
    if force_rebuild or not (os.path.isdir(PERSIST_DIR) and os.listdir(PERSIST_DIR)):
        print("Building index from documents...")
        index = build_index(docs_dir, embed_model_name=EMBED_MODEL, doc_ext=doc_ext)
        print(f"Persisting index to disk at `{PERSIST_DIR}`...")
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        print(f"Loading index from `{PERSIST_DIR}`...")
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    # Create query engine
    print("Creating query engine...")
    query_engine = make_query_engine(
        index=index,
        top_k=top_k,
        mode=prompt_template_mode,
        custom_prompts=custom_prompts,
        temperature=temperature
    )

    # # Print prompts template on the terminal
    # prompts = query_engine.get_prompts()
    # for key, prompt_template in prompts.items():
    #     print(f"\n=== {key} ===\n{prompt_template.get_template()}\n")

    # Execute query
    print("Executing query...")
    response = query_engine.query(query)

    return response