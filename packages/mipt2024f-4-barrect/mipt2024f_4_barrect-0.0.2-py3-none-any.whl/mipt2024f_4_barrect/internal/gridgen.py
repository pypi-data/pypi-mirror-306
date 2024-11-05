import numpy as np
from .gridmap import GridMap


def rect_grid(border: np.ndarray, dest_width: int, dest_height: int) -> GridMap:
    dest_grid = np.int32(
        [
            [0, dest_height],
            [dest_width, dest_height],
            [dest_width, 0],
            [0, 0]
        ]
    )

    return GridMap(border, dest_grid)
