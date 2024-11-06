import numpy as np
import scipy
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

from .utils import squeeze_target


def accuracy(target: np.ndarray, prediction: np.ndarray):
    target = squeeze_target(target)
    if prediction.ndim == 1:
        return accuracy_score(target, prediction)
    return accuracy_score(target, prediction.argmax(axis=1))


def f1(target: np.ndarray, prediction: np.ndarray, **kwargs):
    return f1_score(squeeze_target(target), prediction.argmax(axis=1), **kwargs)


def roc_auc(target: np.ndarray, prediction: np.ndarray, **kwargs):
    target = squeeze_target(target)
    if target.astype(int).max() == 1:
        return roc_auc_score(target, prediction[:, 1])
    return roc_auc_score(target, scipy.special.softmax(prediction, axis=1), **kwargs)


def balanced_log_loss(target: np.ndarray, prediction: np.ndarray):
    N_0 = np.sum(1 - target)
    N_1 = np.sum(target)

    w_0 = 1 / N_0
    w_1 = 1 / N_1

    p_1 = np.clip(prediction, 1e-15, 1 - 1e-15)
    p_0 = 1 - p_1

    log_loss_0 = -np.sum((1 - target) * np.log(p_0))
    log_loss_1 = -np.sum(target * np.log(p_1))

    balanced_log_loss = 2 * (w_0 * log_loss_0 + w_1 * log_loss_1) / (w_0 + w_1)

    return balanced_log_loss / (N_0 + N_1)


def kl_divergence(target: np.ndarray, prediction: np.ndarray, softmax: bool, epsilon: float = 1e-15):
    if softmax:
        prediction = scipy.special.softmax(prediction, axis=1)

    if target.shape == prediction.shape:
        ground_truth = target
    else:
        target = squeeze_target(target).astype(np.int32)  # ndim = 1
        ground_truth = np.zeros_like(prediction)
        ground_truth[np.arange(target.size), target] = 1

    ground_truth = np.clip(ground_truth, epsilon, 1 - epsilon)
    prediction = np.clip(prediction, epsilon, 1 - epsilon)

    return np.sum(ground_truth * np.log(ground_truth / prediction, where=ground_truth > 0)) / len(ground_truth)
