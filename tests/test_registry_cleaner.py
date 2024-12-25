import pytest
from src.registry_cleaner import clean_registry

def test_clean_registry():
    try:
        clean_registry("TestProgram")
        assert True
    except Exception as e:
        pytest.fail(f"Falha ao limpar o registro: {e}")
