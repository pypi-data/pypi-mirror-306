import numpy as np
from sklearn.metrics import mean_absolute_error


def mae(target: np.ndarray, prediction: np.ndarray):
    return mean_absolute_error(target, prediction)
