from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


tags_operation = Table(
    "tags_operation",
    Base.metadata,
    Column("left_id", ForeignKey("tags.id"), primary_key=True),
    Column("right_id", ForeignKey("operation.id"), primary_key=True),
)

tags_info = Table(
    "tags_info",
    Base.metadata,
    Column("left_id", ForeignKey("tags.id"), primary_key=True),
    Column("right_id", ForeignKey("info.id"), primary_key=True),
)

tags_report = Table(
    "tags_report",
    Base.metadata,
    Column("left_id", ForeignKey("tags.id"), primary_key=True),
    Column("right_id", ForeignKey("report.id"), primary_key=True),
)


class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[Optional[str]]

    info: Mapped[list[Report]] = relationship(back_populates="tags")
    report: Mapped[list[Report]] = relationship(back_populates="tags")
    operation: Mapped[list[Report]] = relationship(back_populates="tags")


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

    report: Mapped[Report] = relationship(back_populates="operation")
    tags: Mapped[list[Tags]] = relationship(secondary=tags_operation, back_populates="operation")


class LoadPlan(Base):
    __tablename__ = "load_plan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[Optional[str]]

    steps: Mapped[list[LoadPlanStep]] = relationship(back_populates="plan")
    info: Mapped[list[LoadPlanStep]] = relationship(back_populates="plan")

    @property
    def dump_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class LoadPlanStep(Base):
    __tablename__ = "load_plan_step"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_plan: Mapped[int] = mapped_column(ForeignKey("load_plan.id"))
    id_step: Mapped[int]
    up: Mapped[int]
    hold: Mapped[int]
    down: Mapped[int]
    level: Mapped[float]

    plan: Mapped[LoadPlan] = relationship(back_populates="steps")


class LoadInfo(Base):
    __tablename__ = "info"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_plan: Mapped[int] = mapped_column(ForeignKey("load_plan.id"))
    uuid: Mapped[uuid]
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime]
    start_datetime: Mapped[datetime]
    end_datetime: Mapped[datetime]
    description: Mapped[Optional[str]]

    plan: Mapped[LoadPlan] = relationship(back_populates="info")
    report: Mapped[list[Report]] = relationship(back_populates="info")
    tags: Mapped[list[Tags]] = relationship(secondary=tags_info, back_populates="info")

    @property
    def interval(self) -> timedelta:
        return self.end_datetime - self.end_datetime


class Report(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_info: Mapped[int] = mapped_column(ForeignKey("info.id"))
    id_operation: Mapped[int] = mapped_column(ForeignKey("operation.id"))
    id_metric: Mapped[int] = mapped_column(ForeignKey("metric.id"))
    metric_value: Mapped[float]

    info: Mapped[LoadInfo] = relationship(back_populates="report")
    operation: Mapped[Operation] = relationship(back_populates="report")
    metric: Mapped[Metric] = relationship()
    tags: Mapped[list[Tags]] = relationship(secondary=tags_report, back_populates="report")
