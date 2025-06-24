import os
import sys

# Add parent dir to import the rag module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.auth import Authenticator
from core.sidebar import sidebar
from core.utils import load_yaml, render_example_queries
from rag.main import retrieve_and_query


# --- Init ---
STREAMLIT_DIR = os.path.dirname(os.path.abspath(__file__))
config = load_yaml(f"{STREAMLIT_DIR}/streamlit.yaml")

# --- Streamlit Page Config ---
st.set_page_config(page_title="BBGWiki Chatbot")

# --- User Authentication ---
auth = Authenticator(config=config)
authenticator = auth.require_login()

# --- Sidebar ---
with st.sidebar:
    widgets = sidebar(authenticator)

# --- Chat Interface ---
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- Example Prompts ---
if (
    len(st.session_state.messages) == 1 and
    st.session_state.messages[0]["role"] == "assistant" and
    st.session_state.messages[0]["content"].startswith("How may I assist")
):
    render_example_queries(config)

# --- Handle example prompt if clicked ---
if "pending_query" in st.session_state:
    query = st.session_state.pop("pending_query")
    st.session_state.last_user_query = query
    st.session_state.messages.append({"role": "user", "content": query})
    st.rerun()

# --- User Input ---
if query := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

# --- Generate Assistant Response ---
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            query = st.session_state.messages[-1]['content']
            response = retrieve_and_query(
                query, 
                model=widgets["model"],
                temperature=widgets["temperature"],
                docs_dir=widgets["docs_dir"],
                top_k=widgets["num_chunks"]
                )
            placeholder = st.empty()
            placeholder.markdown(response)


            # # Show where the context came from:
            # for src in response.source_nodes:
            #     path = src.node.extra_info["file_path"]
            #     with st.expander(f"📄 Source"):
            #         st.write(path)

            from pathlib import Path
            for src in response.source_nodes:
                path = src.node.extra_info["file_path"]

                with st.expander(f"📄 {path}"):
                    # read & display the markdown
                    text = Path(path).read_text(encoding="utf-8")
                    st.code(text, language="markdown")

    st.session_state.messages.append({"role": "assistant", "content": str(response)})

