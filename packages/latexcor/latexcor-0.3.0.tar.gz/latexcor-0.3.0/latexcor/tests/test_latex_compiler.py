import pytest
from pathlib import Path
from latexcor.latex_compiler import LatexCompiler
from latexcor.utils import TexFile


def test_get_tex_files(tmp_path):
    # Create temporary .tex files
    (tmp_path / "file1.tex").touch()
    (tmp_path / "file2.tex").touch()
    (tmp_path / "not_tex.txt").touch()

    # Get .tex files
    tex_files = LatexCompiler.get_tex_files(tmp_path)

    # Check if only .tex files are returned
    assert len(tex_files) == 2
    assert all(isinstance(f, TexFile) for f in tex_files)
    assert all(f.name.suffix == ".tex" for f in tex_files)


def test_clean_aux(tmp_path):
    # Create temporary files to be cleaned
    (tmp_path / "test.aux").touch()
    (tmp_path / "test.log").touch()
    (tmp_path / "test.tex").touch()
    (tmp_path / "minted").mkdir()

    # Clean auxiliary files
    LatexCompiler.clean_aux(tmp_path)

    # Check if auxiliary files are removed and .tex file remains
    assert not (tmp_path / "test.aux").exists()
    assert not (tmp_path / "test.log").exists()
    assert not (tmp_path / "minted").exists()
    assert (tmp_path / "test.tex").exists()


# Note: Testing compile_latex and watch methods would require more complex setup and mocking
