import typing as tp

import numpy as np
import pytest

from batch_metric.classification import accuracy
from batch_metric.classification import f1
from batch_metric.classification import kl_divergence
from batch_metric.classification import roc_auc


@pytest.mark.parametrize("case", [
    # Predictions are probabilities
    dict(
        targets=np.array([1, 0, 1, 2]),
        predictions=np.array([
            [0.1, 0, 0.9],
            [0.9, 0.05, 0.05],
            [0.1, 0.2, 0.7],
            [0.1, 0.8, 0.1],
        ]),
        expectation=0.25,
    ),
    # Predictions are not probabilities
    dict(
        targets=np.array([1, 0, 2]),
        predictions=np.array([1, 2, 0]),
        expectation=1 / 3,
    ),
])
def test_accuracy(case: tp.Dict) -> None:
    metric = accuracy(case["targets"], case["predictions"])
    assert abs(metric - case["expectation"]) < 1e-5


@pytest.mark.parametrize("case", [
    dict(
        targets=np.array([1, 1, 1, 0]),
        predictions=np.array([
            [0.1, 0.9],
            [0.9, 0.1],
            [0.3, 0.7],
            [0.8, 0.2],
        ]),
        expectation=2 / 3,
        metric_kwargs=dict(),
    ),
    dict(
        targets=np.array([1, 1, 0, 2]),
        predictions=np.array([
            [0.1, 0, 0.9],
            [0.9, 0.05, 0.05],
            [0.9, 0.05, 0.05],
            [0.1, 0.2, 0.7],
        ]),
        metric_kwargs=dict(average="macro", multi_class="ovr"),
        expectation=0.541666,
    ),
])
def test_roc_auc(case: tp.Dict) -> None:
    metric = roc_auc(case["targets"], case["predictions"], **case["metric_kwargs"])
    assert abs(metric - case["expectation"]) < 1e-5


@pytest.mark.parametrize("case", [
    dict(
        targets=np.array([1, 0, 1, 1]),
        predictions=np.array([
            [0.1, 0.9],
            [0.9, 0.1],
            [0.3, 0.7],
            [0.8, 0.2],
        ]),
        expectation=0.8,
    ),
])
def test_f1_score(case: tp.Dict) -> None:
    metric = f1(case["targets"], case["predictions"])
    assert abs(metric - case["expectation"]) < 1e-5


@pytest.mark.parametrize("case", [
    dict(
        targets=np.array([
            [0.95, 0.05],
            [0.15, 0.85],
        ]),
        predictions=np.array([
            [0.9, 0.1],
            [0.2, 0.8],
        ]),
        expectation=0.01254254,
    ),
    dict(
        targets=np.array([0, 1]),
        predictions=np.array([
            [0.9, 0.1],
            [0.2, 0.8],
        ]),
        expectation=(-np.log(0.9) - np.log(0.8)) / 2,
    ),
    dict(
        targets=np.array([[0.1, 0.8, 0.1]]),
        predictions=np.array([[0.1, 0.7, 0.2]]),
        expectation=(0.8 * np.log(8 / 7) + 0.1 * np.log(0.5)),
    ),
])
def test_kl_divergence(case: tp.Dict) -> None:
    metric = kl_divergence(case["targets"], case["predictions"], softmax=False, epsilon=0)
    assert abs(metric - case["expectation"]) < 1e-5
