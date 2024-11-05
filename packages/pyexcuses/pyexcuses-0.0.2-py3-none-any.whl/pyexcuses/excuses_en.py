# ENGLISH EXCUSES

neutral = [
    "It works on my machine, but maybe the server environment is different.",
    "I think there's a cosmic ray hitting the server at the wrong time.",
    "I'm sure it’s a caching issue—have you tried clearing the cache?",
]

javascript = [
    "The CSS is fighting with JavaScript again.",
    "It's probably because the code's running in sloppy mode instead of strict mode.",
    "I think a stray console.log() is causing interference.",
]

python = [
    "It must be a Python 2 vs. Python 3 issue.",
    "The virtual environment must be acting up.",
    "It worked when I ran it without pytest.",
]

matlab = [
    "It's a rounding error—MATLAB loves its floating-point precision.",
    "It might be a matrix dimension mismatch. MATLAB is picky about that.",
    "I think MATLAB's licensing server must be down again.",
]

excuses_en = {
    "neutral": neutral,
    "python": python,
    "javascript": javascript,
    "matlab": matlab,
    "all": neutral + javascript + python + matlab,
}
