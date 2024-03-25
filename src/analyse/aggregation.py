import abc
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from analyse.metric import MetricAggregationFunction


class AggregationMetric(abc.ABC):
    def __init__(self, data: pd, column_operation: list[str], column_time: str | None, start_datetime: datetime | None):
        self.data = data
        self.column_operation = column_operation
        self.column_time = column_time
        self.start_datetime = start_datetime

    @abc.abstractmethod
    def shift_time(self) -> Any:
        pass

    @abc.abstractmethod
    def metric(self, metric_func: MetricAggregationFunction, column_metric: str) -> None:
        pass


class AggregationStepMetric(AggregationMetric):
    def shift_time(self):
        pass

    def metric(self, metric_func, column_metric: str):
        for shift_level, duration_level in self.shift_time():
            mask_time_start = self.data[self.column_time] >= self.start_datetime + timedelta(minutes=shift_level)
            mask_time_end = self.data[self.column_time] < self.start_datetime + timedelta(
                minutes=shift_level + duration_level)
            data_level = self.data[mask_time_start & mask_time_end].groupby(self.column_operation, dropna=False)[
                column_metric].agg(metric_func)


class AggregationPlatoMetric(AggregationMetric):
    def shift_time(self):
        pass

    def metric(self, metric_func, column_metric: str):
        pass
