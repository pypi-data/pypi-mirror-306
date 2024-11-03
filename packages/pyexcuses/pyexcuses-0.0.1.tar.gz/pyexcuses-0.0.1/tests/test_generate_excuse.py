import pytest
from pyexcuses import pyexcuses
from pyexcuses.exc import SpokenLanguageNotFoundError
from pyexcuses.exc import ProgrammingLanguageNotFoundError


def test_generate_excuse_default():
    """
    Verify generate_excuse() returns a non-empty string.
    """
    actual = (
        pyexcuses.generate_excuse()
    )  # get the actual return value of generate_excuse()
    assert isinstance(
        actual, str
    ), f"Expected generate_excuse() to return a string. Instead, it returned {actual}"
    assert (
        len(actual) > 0
    ), f"Expected generate_excuse() not to be empty. Instead, it returned a string with {len(actual)} characters"


def test_generate_excuse_spanish():
    """
    Verify generate_excuse() returns a non-empty string in spanish mode.
    """
    actual = pyexcuses.generate_excuse(
        spoken_language="es"
    )  # get the actual return value of generate_excuse()
    assert isinstance(
        actual, str
    ), f"Expected generate_excuse() to return a string. Instead, it returned {actual}"
    assert (
        len(actual) > 0
    ), f"Expected generate_excuse() not to be empty. Instead, it returned a string with {len(actual)} characters"


def test_generate_excuse_invalid_spokenlanguage():
    """
    Verify generate_excuse() will fail if given a fake spoken language.
    """
    with pytest.raises(SpokenLanguageNotFoundError) as exception:
        pyexcuses.generate_excuse(spoken_language="no")
    assert isinstance(
        exception.value, SpokenLanguageNotFoundError
    ), f"Expected generate_excuse() to return an error. Instead, it returned {type(exception.value)}"


def test_generate_excuse_invalid_programminglanguage():
    """
    Verify generate_excuse() will fail if given a fake programming language.
    """
    with pytest.raises(ProgrammingLanguageNotFoundError) as exception:
        pyexcuses.generate_excuse(programming_language="c#")
    assert isinstance(
        exception.value, ProgrammingLanguageNotFoundError
    ), f"Expected generate_excuse() to return an error. Instead, it returned {type(exception.value)}"
