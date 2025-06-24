from typing import Optional
from llama_index.core.response_synthesizers.type import ResponseMode
from llama_index.core.prompts.base import Prompt


def make_query_engine(
    index,
    top_k: int = 2,
    mode: str = "compact",
    custom_prompts: Optional[dict] = None,
    temperature: float = 1.0,
):
    """
    Wrap an index into a query engine.
    
    mode: "compact" or "custom".
      - "compact": short answer with citations.
      - "custom": uses your `custom_prompt`.
    """

    engine_kwargs = {
        "similarity_top_k": top_k,
        "response_mode": ResponseMode.COMPACT,
        "verbose": False,
        "response_kwargs": {"temperature": temperature},
    }

    # Only for custom: inject your prompt
    if mode == "custom":
        if custom_prompts is None:
            raise ValueError("custom_prompt must be provided when mode='custom'")
        engine_kwargs["text_qa_template"] = Prompt(custom_prompts["custom"]["qa"])
        engine_kwargs["refine_template"] = Prompt(custom_prompts["custom"]["refine"])

    return index.as_query_engine(**engine_kwargs)