# ENGLISH SOLUTIONS

neutral = [
    "Have you tried adding more comments to your code?",
    "Have you tried turning your computer on and off again?",
    "Try running it on a Friday—bugs don't like weekends.",
]

javascript = [
    "Have you tried adding more semicolons? JavaScript loves them.",
    "Try console.log() the entire function; maybe you’ll spot the issue.",
    "Have you tried switching from var to let or const?",
]

python = [
    "Try adding import this—maybe the Zen of Python has the answer.",
    "Try wrapping it in a try/except and ignore all errors—works like magic!",
    "Maybe switch to a different Python IDE. Sometimes Spyder knows things PyCharm doesn’t.",
]

matlab = [
    "Add a few clc; clear; lines—it might need a fresh workspace.",
    "Re-run the script in single steps; MATLAB is funny about execution order.",
    "Try using the format long command—precision might make all the difference.",
]

solutions_en = {
    "neutral": neutral,
    "python": python,
    "javascript": javascript,
    "matlab": matlab,
    "all": neutral + javascript + python + matlab,
}
