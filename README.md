# NetOpsAI: Telecom Network Operations RAG Assistant

NetOpsAI is a Retrieval-Augmented Generation (RAG) assistant designed for telecom/network operations teams. It helps engineers query telecom manuals, alarm guides, troubleshooting notes, incident reports, and SOP documents using natural language.

## Features

- Upload and ingest telecom knowledge documents
- Supports `.txt`, `.md`, `.pdf`, `.csv`, and `.xlsx`
- FAISS vector database for semantic retrieval
- OpenAI or local HuggingFace embeddings
- Streamlit dashboard
- Telecom-focused troubleshooting assistant
- Source-aware answers
- SQLite incident query logging
- Sample telecom knowledge base included

## Use Cases

- LTE/5G alarm explanation
- BGP and OSPF troubleshooting
- Packet loss investigation
- High VSWR alarm checks
- NOC SOP search
- Incident report summarisation

## Folder Structure

```text
netopsai_project/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   ├── documents/
│   │   └── sample_telecom_knowledge.txt
│   ├── vector_store/
│   └── database/
│
├── src/
│   └── netopsai/
│       ├── __init__.py
│       ├── config.py
│       ├── loaders.py
│       ├── vector_store.py
│       ├── rag_chain.py
│       ├── database.py
│       ├── prompts.py
│       └── utils.py
│
└── tests/
    └── test_basic.py
```

## Installation

```bash
cd netopsai_project
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Copy `.env.example` to `.env`.

```bash
cp .env.example .env
```

For OpenAI mode, add your API key:

```env
OPENAI_API_KEY=your_api_key_here
EMBEDDING_PROVIDER=openai
LLM_PROVIDER=openai
```

For free/local embedding mode:

```env
EMBEDDING_PROVIDER=local
LLM_PROVIDER=openai
```

## Run the App

```bash
streamlit run app.py
```

## How to Use

1. Start the Streamlit app.
2. Click **Build / Rebuild Knowledge Base**.
3. Ask telecom questions such as:
   - What causes high VSWR alarm?
   - How do I troubleshoot BGP neighbour down?
   - What should I check for high packet loss?
   - Summarise LTE handover failure causes.
4. View the answer and document sources.

## Example Questions

```text
What are the steps to troubleshoot high VSWR alarm?
Why is BGP neighbour down?
How should a NOC engineer investigate packet loss?
What are common LTE RRC connection failure causes?
```

## GitHub Portfolio Description

NetOpsAI is a telecom-focused RAG assistant built with Python, Streamlit, LangChain, FAISS, SQLite, and LLMs. It enables network engineers to search telecom manuals, SOPs, alarm guides, and incident reports using natural language. The system retrieves relevant document chunks, generates structured troubleshooting answers, provides source references, and logs user queries for operational review.

## Disclaimer

This project is for educational and portfolio purposes. It should not replace official vendor documentation, certified engineering procedures, or critical network operations processes.
