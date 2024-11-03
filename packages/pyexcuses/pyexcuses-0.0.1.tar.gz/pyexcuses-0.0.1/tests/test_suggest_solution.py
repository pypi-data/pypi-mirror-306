import pytest
from pyexcuses import pyexcuses
from pyexcuses.exc import SpokenLanguageNotFoundError
from pyexcuses.exc import ProgrammingLanguageNotFoundError


def test_suggest_solution_default():
    """
    Verify that suggest_solution() returns a non-empty string.
    """
    actual = (
        pyexcuses.suggest_solution()
    )  # get the actual return value of suggest_solution()
    assert isinstance(
        actual, str
    ), f"Expected suggest_solution() to return a string. Instead, it returned {actual}"
    assert (
        len(actual) > 0
    ), f"Expected suggest_solution() not to be empty. Instead, it returned a string with {len(actual)} characters"


def test_suggest_solution_spanish():
    """
    Verify that suggest_solution() returns a non-empty string in spanish mode.
    """
    actual = pyexcuses.suggest_solution(
        spoken_language="es"
    )  # get the actual return value of suggest_solution()
    assert isinstance(
        actual, str
    ), f"Expected suggest_solution() to return a string. Instead, it returned {actual}"
    assert (
        len(actual) > 0
    ), f"Expected suggest_solution() not to be empty. Instead, it returned a string with {len(actual)} characters"


def test_suggest_solution_invalid_spokenlanguage():
    """
    Verify that suggest_solution() will fail if given a fake spoken language.
    """
    with pytest.raises(SpokenLanguageNotFoundError) as exception:
        pyexcuses.suggest_solution(spoken_language="no")
    assert isinstance(
        exception.value, SpokenLanguageNotFoundError
    ), f"Expected suggest_solution() to return an error. Instead, it returned {type(exception.value)}"


def test_suggest_solution_invalid_programminglanguage():
    """
    Verify that suggest_solution() will fail if given a fake programming language.
    """
    with pytest.raises(ProgrammingLanguageNotFoundError) as exception:
        pyexcuses.suggest_solution(programming_language="c#")
    assert isinstance(
        exception.value, ProgrammingLanguageNotFoundError
    ), f"Expected suggest_solution() to return an error. Instead, it returned {type(exception.value)}"
