import pytest
from pathlib import Path
from latexcor.encoding_converter import EncodingConverter


def test_predict_encoding(tmp_path):
    # Create a temporary file with known encoding
    file_path = tmp_path / "test.tex"
    file_path.write_text("àèç", encoding="utf-8")

    # Test the predict_encoding method
    predicted_encoding = EncodingConverter.predict_encoding(file_path)
    assert predicted_encoding == "utf-8"


def test_convert_utf8(tmp_path):
    # Create a temporary file with non-utf-8 encoding
    file_path = tmp_path / "test.tex"
    file_path.write_text("abc", encoding="windows-1251")

    # Convert the file to UTF-8
    EncodingConverter.convert_utf8(tmp_path)

    # Check if the file is now UTF-8 encoded
    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()
    assert content == "abc"
