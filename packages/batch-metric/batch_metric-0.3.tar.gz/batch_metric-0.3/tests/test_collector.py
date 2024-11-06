import typing as tp
from dataclasses import dataclass

import numpy as np
import pytest

from batch_metric.collector import MetricCalculator


@dataclass
class Batch:
    targets: np.ndarray
    predictions: np.ndarray


@pytest.mark.parametrize("cumulate_history", [True, False])
@pytest.mark.parametrize("case", [
    dict(
        batches=[
            Batch(
                targets=np.array([1, 0, 2]),
                predictions=np.array([1, 0, 2]),
            ),
            Batch(
                targets=np.array([1, 0]),
                predictions=np.array([0, 1]),
            ),
        ],
        func=lambda target, prediction: np.sum(target == prediction) / len(target),
        expectation=0.6,
    ),
    dict(
        batches=[
            Batch(
                targets=np.array([
                    [1, 1],
                    [1, 2],
                ]),
                predictions=np.array([
                    [1, 2],
                    [2, 2],
                ]),
            ),
            Batch(
                targets=np.array([
                    [2, 3],
                ]),
                predictions=np.array([
                    [3, 2],
                ]),
            ),
        ],
        func=lambda target, prediction: np.sum(target == prediction) / target.shape[0] / target.shape[1],
        expectation=1 / 3,
    ),
])
def test(cumulate_history: bool, case: tp.Dict) -> None:
    metric = MetricCalculator(
        func=case["func"],
        metric_kwargs=dict(),
        cumulate_history=cumulate_history,
    )
    for data in case["batches"]:
        metric.update(data.targets, data.predictions)

    assert abs(metric.compute() - case["expectation"]) < 1e-5
