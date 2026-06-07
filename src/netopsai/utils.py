from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".csv", ".xlsx"}


def is_supported_file(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def clean_text(text: str) -> str:
    return " ".join(text.replace("\x00", " ").split())


def list_supported_files(directory: Path) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    return [p for p in directory.rglob("*") if p.is_file() and is_supported_file(p)]
