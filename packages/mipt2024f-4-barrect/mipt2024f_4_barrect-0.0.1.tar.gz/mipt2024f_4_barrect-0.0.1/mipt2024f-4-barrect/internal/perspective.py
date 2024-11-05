import cv2
import numpy as np


def warp_perspective(
        img_src: np.ndarray,
        point_src: np.ndarray,
        point_dest: np.ndarray,
        width: int,
        height: int
) -> np.ndarray:
    matrix = cv2.getPerspectiveTransform(point_src, point_dest)
    return cv2.warpPerspective(img_src, matrix, (width, height))
