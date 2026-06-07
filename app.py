import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.netopsai.config import Settings
from src.netopsai.database import init_db, log_query, get_recent_queries
from src.netopsai.loaders import save_uploaded_files
from src.netopsai.rag_chain import build_answer
from src.netopsai.vector_store import build_vector_store, load_vector_store


load_dotenv()

st.set_page_config(
    page_title="NetOpsAI - Telecom RAG Assistant",
    page_icon="📡",
    layout="wide",
)

settings = Settings()
init_db(settings.database_path)

st.title("📡 NetOpsAI: Telecom Network Operations RAG Assistant")
st.write(
    "Ask telecom/network operations questions from manuals, SOPs, alarm guides, logs, "
    "incident reports, and troubleshooting documents."
)

with st.sidebar:
    st.header("Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload telecom documents",
        type=["txt", "md", "pdf", "csv", "xlsx"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        saved = save_uploaded_files(uploaded_files, settings.documents_dir)
        st.success(f"Saved {len(saved)} file(s).")

    if st.button("Build / Rebuild Knowledge Base"):
        with st.spinner("Building FAISS vector store..."):
            count = build_vector_store(settings)
        st.success(f"Knowledge base built with {count} document chunks.")

    st.divider()
    st.subheader("Settings")
    st.write(f"Embedding provider: `{settings.embedding_provider}`")
    st.write(f"LLM provider: `{settings.llm_provider}`")
    st.write(f"Top-K retrieval: `{settings.top_k}`")

    st.divider()
    st.subheader("Recent Queries")
    recent = get_recent_queries(settings.database_path, limit=5)
    for item in recent:
        st.caption(f"{item['created_at']} — {item['question'][:80]}")

tab1, tab2, tab3 = st.tabs(["Ask NetOpsAI", "Sample Questions", "Project Notes"])

with tab1:
    question = st.text_area(
        "Enter your telecom/network operations question",
        placeholder="Example: What are the steps to troubleshoot high VSWR alarm?",
        height=120,
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        ask = st.button("Ask", type="primary")

    if ask:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                vector_store = load_vector_store(settings)
                with st.spinner("Retrieving knowledge and generating answer..."):
                    result = build_answer(question, vector_store, settings)

                log_query(
                    db_path=settings.database_path,
                    question=question,
                    answer=result["answer"],
                    sources=result["sources"],
                )

                st.subheader("Answer")
                st.markdown(result["answer"])

                st.subheader("Sources")
                if result["sources"]:
                    for source in result["sources"]:
                        st.info(
                            f"**File:** {source.get('source', 'Unknown')}  \n"
                            f"**Preview:** {source.get('preview', '')}"
                        )
                else:
                    st.write("No sources returned.")

            except FileNotFoundError:
                st.error(
                    "Vector store not found. Please build the knowledge base from the sidebar first."
                )
            except Exception as exc:
                st.error(f"Error: {exc}")

with tab2:
    st.subheader("Try These Questions")
    examples = [
        "What are common causes of high VSWR alarm?",
        "How do I troubleshoot BGP neighbour down?",
        "What should I check when users report high packet loss?",
        "Explain LTE RRC connection failure causes.",
        "What steps should a NOC engineer follow during a site outage?",
        "How can I investigate OSPF adjacency down?",
    ]
    for q in examples:
        st.code(q)

with tab3:
    st.subheader("About This Project")
    st.write(
        """
        NetOpsAI demonstrates a real-world RAG architecture for telecom network operations.
        It is suitable for a GitHub portfolio, academic submission, or AI engineering interview project.
        """
    )
    st.markdown(
        """
        **Main components:**
        - Document ingestion
        - Text chunking
        - Embedding generation
        - FAISS vector search
        - LLM answer generation
        - Source citation
        - SQLite query logging
        - Streamlit frontend
        """
    )
