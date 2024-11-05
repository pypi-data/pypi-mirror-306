import random
from typing import Any, Generator, Literal, get_args

from .excuses_en import excuses_en
from .excuses_es import excuses_es
from .solutions_en import solutions_en
from .solutions_es import solutions_es
from .exc import SpokenLanguageNotFoundError
from .exc import ProgrammingLanguageNotFoundError

all_excuses = {
    "en": excuses_en,
    "es": excuses_es,
}

all_solutions = {
    "en": solutions_en,
    "es": solutions_es,
}

SPOKEN_LANGUAGES = Literal["en", "es"]
PROGRAMMING_LANGUAGES = Literal["neutral", "javascript", "python", "matlab", "all"]

SPOKENLANGUAGE_VALUES = set(get_args(SPOKEN_LANGUAGES))
PROGRAMMINGLANGUAGE_VALUES = set(get_args(PROGRAMMING_LANGUAGES))


def suggest_solution(
    spoken_language: SPOKEN_LANGUAGES = "en",
    programming_language: PROGRAMMING_LANGUAGES = "neutral",
) -> str:
    """
    Suggest a solution for the given spoken and programming languages
    """
    try:
        solutions = all_solutions[spoken_language]
    except KeyError:
        raise SpokenLanguageNotFoundError("That spoken language isn't in our system ):")

    try:
        return random.choice(solutions[programming_language])
    except KeyError:
        raise ProgrammingLanguageNotFoundError(
            "That programming language isn't in our system ):"
        )


def generate_excuse(
    spoken_language: SPOKEN_LANGUAGES = "en",
    programming_language: PROGRAMMING_LANGUAGES = "neutral",
) -> str:
    """
    Generate an excuse for the given spoken and programming languages
    """
    try:
        excuses = all_excuses[spoken_language]
    except KeyError:
        raise SpokenLanguageNotFoundError("That spoken language isn't in our system ):")

    try:
        return random.choice(excuses[programming_language])
    except KeyError:
        raise ProgrammingLanguageNotFoundError(
            "That programming language isn't in our system ):"
        )


def list_available_options(
    option_type: Literal["spoken_language", "programming_language"]
) -> list[str]:
    """
    Lists available spoken or programming languages based on the option type.
    """
    if option_type == "spoken_language":
        return list(SPOKENLANGUAGE_VALUES)
    elif option_type == "programming_language":
        return list(PROGRAMMINGLANGUAGE_VALUES)
    else:
        raise ValueError(
            "Invalid option type. Choose either 'spoken_language' or 'programming_language'."
        )


def get_multilingual_excuse_or_solution(
    option_type: Literal["excuse", "solution"],
    programming_language: PROGRAMMING_LANGUAGES = "neutral",
) -> dict[str, str]:
    """
    Retrieve a random excuse or solution in both 'en' and 'es' for the given programming language.
    """
    results = {}
    for lang in SPOKENLANGUAGE_VALUES:
        try:
            if option_type == "excuse":
                results[lang] = generate_excuse(lang, programming_language)
            elif option_type == "solution":
                results[lang] = suggest_solution(lang, programming_language)
            else:
                raise ValueError(
                    "Invalid option type. Choose either 'excuse' or 'solution'."
                )
        except (SpokenLanguageNotFoundError, ProgrammingLanguageNotFoundError):
            results[lang] = "No available option"
    return results
