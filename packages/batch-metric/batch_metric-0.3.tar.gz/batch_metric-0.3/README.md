# batch-metric

Install:

```bash
pip install batch-metric
```

Example:

```python
import numpy as np
from batch_metric.collector import MetricCalculator
from batch_metric.classification import accuracy

metric_calculator = MetricCalculator(
    func=accuracy,
    metric_kwargs=dict(),
    cumulate_history=False,
)
metric_calculator.update(
    np.array([1, 0, 1, 2]),
    np.array([
        [0.1, 0.0, 0.9],
        [0.6, 0.3, 0.1],
        [0.1, 0.2, 0.7],
        [0.1, 0.8, 0.1],
    ]))

print(metric_calculator.compute())
```