# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

## Installation

Install the `pyexcuses` module with pip:

```console
pip3 install pyexcuses
```

### Python

Access the **excuses** in your own project by importing `pyexcuses` and using the function
`generate_excuse`:

```pycon
>>> import pyexcuses
>>> print(pyexcuses.generate_excuse())
It works on my machine, but maybe the server environment is different.
```

We can use spoken languages for English and Spanish, and we have excuses for different programming languages:

```pycon
>>> import pyexcuses
>>> print(pyexcuses.generate_excuse("es"))  # spanish excuse
Funciona en mi máquina, pero quizás el entorno del servidor sea diferente
>>> print(pyexcuses.generate_excuse("es", "javascript"))  # spanish excuse for javascript programming language
El CSS está luchando con JavaScript de nuevo.
```

Access the **solutions** in your own project by importing `pyexcuses` and using the function
`suggest_solution`:

```pycon
>>> import pyexcuses
>>> print(pyexcuses.suggest_solution())
Try running it on a Friday—bugs don't like weekends.
```

Similarly, we have solutions for different languages and programming languages:

```pycon
>>> import pyexcuses
>>> print(pyexcuses.suggest_solution("es"))  # spanish solution
"¿Has probado a añadir más comentarios a tu código?
>>> print(pyexcuses.suggest_solution("es", "javascript"))  # spanish solution for javascript programming language
¿Has probado a añadir más puntos y comas? A JavaScript le encantan.
```

## Team members

- [Darren Zou](https://github.com/darrenzou)
- [Peter D'Angelo](https://github.com/dangelo729)
- [Gene Park](https://github.com/geneparkmcs)
- [Joseph Chege](https://github.com/JosephChege4)
