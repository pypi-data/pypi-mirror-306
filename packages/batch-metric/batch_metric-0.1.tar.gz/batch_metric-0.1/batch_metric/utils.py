import numpy as np


def squeeze_target(target: np.ndarray) -> np.ndarray:
    """
    Squeezes targets into 1 dimension tensor. This function is useful for calculation classification metrics which most
    of them take 1 dimension targets. Some Datasets can return different target shapes, as example:
        * [1, 2, 3] -> [1, 2, 3]
        * [[1], [2], [1]] -> [1, 2, 3]
        * [[1]] -> [1]
    """
    target = target.squeeze()
    if target.ndim == 0:
        target = np.array([target], dtype=int)
    return target
