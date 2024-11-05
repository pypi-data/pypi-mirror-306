import numpy as np


class GridMap:
    src: np.ndarray
    dest: np.ndarray

    def __init__(self, src: np.ndarray, dest: np.ndarray):
        self.src = src
        self.dest = dest
