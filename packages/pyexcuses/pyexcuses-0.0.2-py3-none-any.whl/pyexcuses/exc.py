class PyexcusesError(Exception):
    "Base class for all pyexcuses exceptions"


class SpokenLanguageNotFoundError(PyexcusesError):
    pass


class ProgrammingLanguageNotFoundError(PyexcusesError):
    pass
