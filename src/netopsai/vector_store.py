from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from .config import Settings
from .loaders import load_documents, split_documents


def get_embeddings(settings: Settings):
    if settings.embedding_provider.lower() == "openai":
        return OpenAIEmbeddings(model=settings.openai_embedding_model)

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_vector_store(settings: Settings) -> int:
    settings.ensure_dirs()

    documents = load_documents(settings.documents_dir)
    if not documents:
        raise ValueError(
            f"No supported documents found in {settings.documents_dir}. "
            "Add .txt, .md, .pdf, .csv, or .xlsx files."
        )

    chunks = split_documents(
        documents,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    embeddings = get_embeddings(settings)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(str(settings.vector_store_dir))

    return len(chunks)


def load_vector_store(settings: Settings):
    embeddings = get_embeddings(settings)
    index_file = settings.vector_store_dir / "index.faiss"

    if not index_file.exists():
        raise FileNotFoundError("FAISS vector store not found.")

    return FAISS.load_local(
        str(settings.vector_store_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )
