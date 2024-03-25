from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Metric(Base):
    __tablename__ = "metric"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[Optional[str]]


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[Optional[str]]

    report_operation: Mapped[ReportOperation] = relationship(back_populates="operation")


class ReportInfo(Base):
    __tablename__ = "report_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    # id_profile: Mapped
    # uuid: Mapped[uuid]
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime]
    start_datetime: Mapped[datetime]
    end_datetime: Mapped[datetime]
    description: Mapped[Optional[str]]

    # report_operation

    @property
    def interval(self) -> timedelta:
        return self.end_datetime - self.end_datetime


class ReportOperation(Base):
    __tablename__ = "report_operation"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_report: Mapped[int] = mapped_column(ForeignKey("report_info.id"))
    id_operation: Mapped[int] = mapped_column(ForeignKey("operation.id"))
    id_metric: Mapped[int] = mapped_column(ForeignKey("metric.id"))
    metric_value: Mapped[float]
    # id_plan_level: Mapped

    operation: Mapped[Operation] = relationship(back_populates="report_operation")
