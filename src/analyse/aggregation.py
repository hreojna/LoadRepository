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

    def __init__(self, *args,
                 load_plan: list,
                 offset: int = None,
                 offset_left: int = 0,
                 offset_right: int = 0,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if offset:
            self.offset_left = offset
            self.offset_right = offset
        else:
            self.offset_left = offset_left
            self.offset_right = offset_right
        self.load_plan = load_plan

    def shift_time(self):
        shift_time = 0
        for step in self.load_plan:
            up_time = step[0]
            hold_time = step[1]
            down_time = step[2]
            load_level = step[3]
            duration = hold_time - self.offset_left - self.offset_right
            shift_time = up_time + shift_time
            yield shift_time + self.offset_left, duration, load_level
            shift_time += hold_time + down_time

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
