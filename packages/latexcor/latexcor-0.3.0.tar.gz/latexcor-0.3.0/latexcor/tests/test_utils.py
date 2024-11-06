import pytest
from pathlib import Path
from latexcor.utils import TexFile


def test_tex_file():
    # Create a TexFile instance
    file_path = Path("/path/to/file.tex")
    tex_file = TexFile(
        name=file_path, time_modification=1234567890.0, path=file_path.parent
    )

    # Check if the attributes are set correctly
    assert tex_file.name == file_path
    time1 = tex_file.time_modification
    assert tex_file.time_modification == 1234567890.0
    assert tex_file.path == file_path.parent

    # Check string representation
    # assert str(tex_file) == f"TexFile(name={file_path}, time_modification=1234567890.0, path={file_path.parent})"

    # Check equality
    tex_file2 = TexFile(
        name=file_path, time_modification=1234567890.0, path=file_path.parent
    )
    assert tex_file == tex_file2

    # Check inequality
    tex_file3 = TexFile(
        name=file_path, time_modification=9876543210.0, path=file_path.parent
    )
    assert tex_file != tex_file3
