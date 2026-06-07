from src.netopsai.utils import clean_text, is_supported_file
from pathlib import Path


def test_clean_text():
    assert clean_text("hello\n\nworld") == "hello world"


def test_supported_file():
    assert is_supported_file(Path("manual.pdf")) is True
    assert is_supported_file(Path("image.png")) is False
