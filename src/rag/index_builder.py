from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import SimpleDirectoryReader

def build_index(
    docs_dir: str,
    embed_model_name: str = "baai/bge-small-en-v1.5",
    chunk_size: int = 256,
    chunk_overlap: int = 10,
    doc_ext: list[str] = [".md"]
):
    # Load documents
    reader = SimpleDirectoryReader(
        input_dir=docs_dir,
        recursive=True,
        required_exts=doc_ext
    )
    documents = reader.load_data()

    # Create a storage context (no extra docstore needed)
    storage_context = StorageContext.from_defaults()

    # Embedder & splitter
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
    splitter = TokenTextSplitter(
        separator=" ",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Build the index
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        embed_model=embed_model,
        transformations=[splitter],
    )

    return index