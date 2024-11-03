import pytest
from pyexcuses import pyexcuses

def test_list_available_options_spoken_language():
    result = pyexcuses.list_available_options("spoken_language")
    assert isinstance(result, list)
    assert "en" in result
    assert "es" in result

def test_list_available_options_programming_language():
    result = pyexcuses.list_available_options("programming_language")
    assert isinstance(result, list)
    assert "neutral" in result
    assert "javascript" in result
    assert "python" in result

def test_list_available_options_invalid_type():
    with pytest.raises(ValueError, match="Invalid option type. Choose either 'spoken_language' or 'programming_language'."):
        pyexcuses.list_available_options("invalid_type")

