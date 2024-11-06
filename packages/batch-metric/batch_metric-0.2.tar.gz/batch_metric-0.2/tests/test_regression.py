import typing as tp

import numpy as np
import pytest

from batch_metric.regression import mae


@pytest.mark.parametrize("case", [
    dict(
        targets=np.array([1, 0, 2]),
        predictions=np.array([1, 2, 0]),
        expectation=4 / 3,
    ),
])
def test_accuracy(case: tp.Dict) -> None:
    metric = mae(case["targets"], case["predictions"])
    assert abs(metric - case["expectation"]) < 1e-5
