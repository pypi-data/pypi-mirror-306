import pytest
from pathlib import Path
from latexcor.file_manager import FileManager


def test_slugify_files(tmp_path, monkeypatch):
    # Create temporary files and directories
    (tmp_path / "Test File.tex").touch()
    (tmp_path / "Another Test").mkdir()

    # Mock the input function to always return 'y'
    monkeypatch.setattr("builtins.input", lambda _: "y")

    # Run the slugify_files method
    FileManager.slugify_files(tmp_path, automatic=False)

    # Check if files and directories have been renamed
    assert (tmp_path / "test-file.tex").exists()
    assert (tmp_path / "another-test").exists()
    assert not (tmp_path / "Test File.tex").exists()
    assert not (tmp_path / "Another Test").exists()
