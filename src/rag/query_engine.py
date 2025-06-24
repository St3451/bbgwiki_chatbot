def make_query_engine(index, top_k: int = 2, mode: str = "compact", custom_prompt=None):
    """
    Wrap an index into a query engine.
    mode: one of "compact", "verbose", "tree_summarize", or "custom"
    """
    params = {
        "similarity_top_k": top_k,
        "response_mode": mode,
    }
    if mode == "custom" and custom_prompt is not None:
        params["custom_prompt"] = custom_prompt

    return index.as_query_engine(**params)