from __future__ import annotations
import streamlit as st
import os
from PIL import Image
from typing import Any


def render_logo() -> None:
    """
    Renders the logo and application title in the sidebar.
    """
    path=f"{os.path.dirname(os.path.abspath(__file__))}/../assets/bbglab_logo.png"
    icon = Image.open(path)
    _, col2, _ = st.columns([1, 3, 1])
    with col2:
        st.image(icon)


def sidebar(authenticator: Any) -> str:
    """
    Renders the sidebar UI and returns the selected model.
    """

    render_logo()
    st.title("BBGWiki Chatbot")

    # Session Info
    st.subheader("👤 User Session")
    authenticator.logout("↩️ Logout", location="sidebar")

    # Settings
    st.markdown("---")
    st.subheader('🧠 Model')
    widgets = {}

    widgets["model"] = st.selectbox(
        label="LLM",
        options=["gpt-3.5-turbo", "gpt-4o-mini"],
        key="selected_model",
        help="Choose which language model to use for answering your questions"
    )

    widgets["temperature"] = st.slider(
        label="Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,    
        step=0.1,
        help="Controls randomness of the model: 0.0 (deterministic) → 2.0 (very random)"
    )

    widgets["use_custom"] = st.checkbox(
        label="Use custom prompt",
        value=False,
        help="Check to use your own prompt template in './config/prompts.yaml' instead of the built-in template"
    )
    widgets["mode"] = "custom" if widgets["use_custom"] else "compact"

    st.markdown("---")
    st.subheader('🔍 Context Retrieval')

    widgets["docs_dir"] = st.text_input(
        label="Path to your documents",
        value="./bbgwiki/docs/",
        placeholder="e.g. ./bbgwiki/docs/BBGProtocols/",
        help="Filesystem path where your files are stored"
    )

    widgets["doc_ext"] = st.multiselect(
        label="Document file extensions",
        options=[".md", ".txt", ".pdf", ".docx"],
        default=[".md"],
        help="Only files with these extensions will be loaded into the index"
    )

    widgets["num_chunks"] = st.slider(
        label="Number of chunks",
        min_value=1,
        max_value=5,
        value=2,        
        step=1,
        help="How many document chunks to retrieve per query for context"
    )

    widgets["force_rebuild"] = st.checkbox(
        label="Force rebuild index",
        value=False,
        help="If checked, will rebuild and re-persist the vector store on every query"
    )

    # Learn More
    st.markdown("---")
    st.subheader("📖 Learn more")
    st.markdown("[BBGWiki](https://bbglab.github.io/bbgwiki/)")
    st.markdown("[BBGWiki GitHub](https://github.com/bbglab/bbgwiki)")

    return widgets

