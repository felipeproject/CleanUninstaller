import pytest
from src.file_cleaner import clean_files
import os

def test_clean_files(tmp_path):
    test_dir = tmp_path / "TestProgram"
    test_dir.mkdir()
    clean_files(tmp_path, "TestProgram")
    assert not os.path.exists(test_dir)
