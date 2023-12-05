from enum import Enum
from statistics import mean, median, mode
from functools import partial


class Aggregation(Enum):
    MEDIAN = partial(median)
    MEAN = partial(mean)
    MODE = partial(mode)
    COUNT = len
    MIN = min
    MAX = max
