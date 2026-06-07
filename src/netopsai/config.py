import os
from pathlib import Path
from pydantic import BaseModel, Field


class Settings(BaseModel):
    project_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])
    documents_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data" / "documents")
    vector_store_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data" / "vector_store")
    database_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data" / "database" / "netopsai.db")

    embedding_provider: str = Field(default_factory=lambda: os.getenv("EMBEDDING_PROVIDER", "local"))
    llm_provider: str = Field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"))

    openai_chat_model: str = Field(default_factory=lambda: os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"))
    openai_embedding_model: str = Field(default_factory=lambda: os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

    chunk_size: int = Field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "900")))
    chunk_overlap: int = Field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "150")))
    top_k: int = Field(default_factory=lambda: int(os.getenv("TOP_K", "4")))

    def ensure_dirs(self) -> None:
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        self.vector_store_dir.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
