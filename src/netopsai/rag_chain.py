from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from .config import Settings
from .prompts import SYSTEM_PROMPT


def get_llm(settings: Settings):
    if settings.llm_provider.lower() == "openai":
        return ChatOpenAI(
            model=settings.openai_chat_model,
            temperature=0.2,
        )

    raise ValueError("Only OpenAI LLM provider is configured in this version.")


def format_context(docs) -> str:
    blocks = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Unknown source")
        content = doc.page_content
        blocks.append(f"[Source {i}: {source}]\n{content}")
    return "\n\n".join(blocks)


def build_answer(question: str, vector_store, settings: Settings) -> dict:
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.top_k},
    )

    docs = retriever.invoke(question)
    context = format_context(docs)

    user_prompt = f"""
Question:
{question}

Retrieved context:
{context}

Generate a telecom network operations answer using the required structured format.
"""

    llm = get_llm(settings)
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt),
        ]
    )

    sources = []
    for doc in docs:
        preview = doc.page_content[:250].replace("\n", " ")
        sources.append(
            {
                "source": doc.metadata.get("source", "Unknown"),
                "preview": preview + ("..." if len(doc.page_content) > 250 else ""),
            }
        )

    return {
        "answer": response.content,
        "sources": sources,
    }
