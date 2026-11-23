import math

from . import Task1 as t1
from . import Task3 as t3
from . import Task5 as t5

# Classes

class Signal():
    def __init__(self, cont: bool, sig: dict):
        self.type = cont
        self.sig = {}
        self.func = None
        if self.type:
            self.func = lambda t: sig["A"] * sig["func"]((2 * math.pi * sig["f"]/sig["fs"]) * t + sig["theta"])
            
            self.sig = {(2 * math.pi * sig["f"]/sig["fs"])*n: self.func(n) for n in sig["s_range"]}
        else:
            self.sig = sig

# Globals

TASKS = ["Task 1", "Task 2", "Task 3", "Task 5"]
N_SAMPLES = None
SIGNALS: dict[str, Signal] = {}
SIG_NUM = 0
MAX_LINES = 200
LEVEL_COLORS = {
    "info":  (200, 200, 200),
    "ok":    (80, 255, 120),
    "warn":  (240, 190, 60),
    "error": (240, 80, 80),
}