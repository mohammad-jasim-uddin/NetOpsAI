from pathlib import Path
from typing import Iterable

import pandas as pd
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .utils import clean_text, list_supported_files


def save_uploaded_files(uploaded_files, documents_dir: Path) -> list[Path]:
    documents_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for uploaded in uploaded_files:
        safe_name = uploaded.name.replace("/", "_").replace("\\", "_")
        path = documents_dir / safe_name
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        saved_paths.append(path)

    return saved_paths


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)


def read_csv_file(path: Path) -> str:
    df = pd.read_csv(path)
    return df.to_string(index=False)


def read_excel_file(path: Path) -> str:
    excel = pd.ExcelFile(path)
    parts = []
    for sheet in excel.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        parts.append(f"Sheet: {sheet}\n{df.to_string(index=False)}")
    return "\n\n".join(parts)


def load_single_file(path: Path) -> Document:
    suffix = path.suffix.lower()

    if suffix in [".txt", ".md"]:
        text = read_text_file(path)
    elif suffix == ".pdf":
        text = read_pdf_file(path)
    elif suffix == ".csv":
        text = read_csv_file(path)
    elif suffix == ".xlsx":
        text = read_excel_file(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    text = clean_text(text)

    return Document(
        page_content=text,
        metadata={
            "source": path.name,
            "path": str(path),
        },
    )


def load_documents(documents_dir: Path) -> list[Document]:
    files = list_supported_files(documents_dir)
    docs = []

    for path in files:
        try:
            doc = load_single_file(path)
            if doc.page_content.strip():
                docs.append(doc)
        except Exception as exc:
            print(f"Could not load {path}: {exc}")

    return docs


def split_documents(documents: list[Document], chunk_size: int, chunk_overlap: int) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)
