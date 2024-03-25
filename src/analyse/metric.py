from __future__ import annotations

from typing import Protocol, Any

import numpy as np
import pandas as pd

register: list[MetricAggregationFunction] = list()


class MetricAggregationFunction(Protocol):
    metric_name: str
    precision: int
    description: str

    def __call__(self, x: pd.Series | pd.DataFrame) -> Any:
        pass


def metric_analyse(name: str, precision: int = 0, description: str | None = None):
    def _wrapper(func: MetricAggregationFunction):
        register.append(func)
        func.metric_name = name
        func.precision = precision
        func.description = description
        return func

    return _wrapper


@metric_analyse('rpm', 0, 'количество запросов в минуту')
def rpm(x: pd.Series, **kwargs):
    return np.sum(x) / kwargs['duration_time']


@metric_analyse('avg', 0, 'среднее время обрабтки запросов')
def avg(x: pd.Series):
    return np.average(x)
