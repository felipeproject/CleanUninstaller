import pytest
from src.uninstaller import list_installed_programs, uninstall_program

def test_list_installed_programs():
    programs = list_installed_programs()
    assert isinstance(programs, list)

def test_uninstall_program():
    result = uninstall_program("ProgramName")
    assert result in [True, "ProgramName not found"]
