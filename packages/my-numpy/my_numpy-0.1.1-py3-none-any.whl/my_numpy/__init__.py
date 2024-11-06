# my_numpy/__init__.py

from .stats import mean
from .stats import median

# for (from my_numpy.stats import *) to work
__all__ = ["mean", "median"]
