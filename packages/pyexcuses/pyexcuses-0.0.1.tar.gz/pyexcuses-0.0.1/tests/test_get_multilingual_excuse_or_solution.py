import pytest
from pyexcuses import pyexcuses

def test_get_multilingual_excuse_or_solution_excuse():
    result = pyexcuses.get_multilingual_excuse_or_solution("excuse", "python")
    assert isinstance(result, dict)
    assert "en" in result and isinstance(result["en"], str)
    assert "es" in result and isinstance(result["es"], str)

def test_get_multilingual_excuse_or_solution_solution():
    result = pyexcuses.get_multilingual_excuse_or_solution("solution", "javascript")
    assert isinstance(result, dict)
    assert "en" in result and isinstance(result["en"], str)
    assert "es" in result and isinstance(result["es"], str)

def test_get_multilingual_excuse_or_solution_invalid_type():
    with pytest.raises(ValueError, match="Invalid option type. Choose either 'excuse' or 'solution'."):
        pyexcuses.get_multilingual_excuse_or_solution("invalid_type", "python")

def test_get_multilingual_excuse_or_solution_unsupported_language():
    # Mock unsupported language by adding exception handling, assuming generate_excuse and suggest_solution will raise the error
    result = pyexcuses.get_multilingual_excuse_or_solution("excuse", "unsupported_language")
    assert result["en"] == "No available option"
    assert result["es"] == "No available option"
