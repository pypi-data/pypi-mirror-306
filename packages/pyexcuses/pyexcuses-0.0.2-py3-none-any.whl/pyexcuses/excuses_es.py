# SPANISH EXCUSES

neutral = [
    "Funciona en mi máquina, pero quizás el entorno del servidor sea diferente.",
    "Creo que un rayo cósmico está impactando al servidor en el momento equivocado.",
    "Estoy seguro de que es un problema de caché. ¿Has intentado borrar el caché?",
]

javascript = [
    "El CSS está luchando con JavaScript de nuevo.",
    "Probablemente se deba a que el código se está ejecutando en modo descuidado en lugar de en modo estricto.",
    "Creo que un console.log() extraviado está causando interferencias.",
]

python = [
    "Debe ser un problema de Python 2 vs. Python 3.",
    "El entorno virtual debe estar funcionando mal.",
    "Funcionó cuando lo ejecuté sin pytest.",
]

matlab = [
    "Es un error de redondeo; a MATLAB le encanta su precisión de punto flotante.",
    "Podría ser una discrepancia en la dimensión de la matriz. MATLAB es muy exigente con eso.",
    "Creo que el servidor de licencias de MATLAB debe estar inactivo nuevamente.",
]

excuses_es = {
    "neutral": neutral,
    "python": python,
    "javascript": javascript,
    "matlab": matlab,
    "all": neutral + javascript + python + matlab,
}
