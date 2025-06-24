from __future__ import annotations
import streamlit as st
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader


def load_yaml(path: str):
    """
    Load configuration
    """
    with open(path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


def render_example_queries(config) -> None:
    """
    Renders a grid of clickable example queries to inject into the chat.
    """
    example_prompts = config["example_queries"]
    cols = st.columns(2)
    for i, prompt_text in enumerate(example_prompts):
        if cols[i % 2].button(prompt_text, key=f"example_query_{i}"):
            st.session_state["pending_query"] = prompt_text
            st.rerun()