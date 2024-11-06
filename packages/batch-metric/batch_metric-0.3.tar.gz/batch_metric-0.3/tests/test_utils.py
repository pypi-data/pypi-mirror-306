import numpy as np
import pytest

from batch_metric.utils import squeeze_target


@pytest.mark.parametrize("target", [
    np.array([1, 2, 3]),
    np.array([[1], [2], [3]]),
    np.array([1]),
])
def test_squeeze_target(target: np.ndarray) -> None:
    assert squeeze_target(target).ndim == 1
