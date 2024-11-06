import typing as tp

import numpy as np


class MetricCalculator:
    """
    Metric provide a way to compute metrics without having to store the entire output history of a model.
    NOTE: some metrics require all targets and predictions. For example ROC_AUC
    NOTE: self.func must use numpy arrays as inputs
    """

    def __init__(self, *, func: tp.Callable, metric_kwargs: tp.Dict[str, tp.Any], cumulate_history: bool):
        self.func: tp.Callable = func
        self.metric_kwargs = metric_kwargs
        self.count: int = 0
        self.cumulative_score: float = 0.0
        self.cumulate_history = cumulate_history

        if self.cumulate_history:
            self.targets = []
            self.predictions = []

    def update(self, target: np.ndarray, prediction: np.ndarray):
        if self.cumulate_history:
            self.targets.append(target)
            self.predictions.append(prediction)
        else:
            score = self.func(target, prediction, **self.metric_kwargs)
            self.count += len(target)
            self.cumulative_score += score * len(target)

    def compute(self):
        if self.cumulate_history:
            if self.targets:
                return self.func(np.concatenate(self.targets), np.concatenate(self.predictions), **self.metric_kwargs)
            else:
                raise Exception("There is no cumulated targets and predictions to calculate metric!")
        elif self.count:
            return self.cumulative_score / self.count
        else:
            raise Exception("There is no self.cumulative_score and self.count in order to average metric!")
