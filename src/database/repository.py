import abc
import logging
from functools import singledispatchmethod

from psycopg2 import errors
from sqlalchemy import exc, delete
from sqlalchemy.orm import Session, DeclarativeBase

from database.model import LoadInfo, Metric, Report, Operation, LoadPlan

logger = logging.getLogger(__name__)


class AbstractRepository(abc.ABC):

    def __init__(self, session):
        self.__session: Session = session

    def add(self, obj):
        try:
            self.session.add(obj)
        except exc.IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                logger.warning(f'The {obj} is already in the table {obj.__tablename__}')
            else:
                raise e
        else:
            self.session.commit()
            logger.info(f'Added new {obj} to the table {obj.__tablename__}')
        return obj

    def add_all(self, objs: list):
        try:
            self.session.add_all(objs)
        except exc.IntegrityError as e:
            self.session.rollback()
            raise e
        else:
            self.session.commit()
        return objs

    @singledispatchmethod
    def delete(self, obj):
        pass

    @delete.register
    def _delete(self, obj: int):
        self.session.execute(delete(self.table).where(self.table.c.id == obj))

    @delete.register
    def _delete(self, obj: DeclarativeBase):
        self.session.execute(delete(obj.__table__).where(obj.__table__.c.id == obj.id))

    @property
    @abc.abstractmethod
    def table(self):
        pass

    @property
    def session(self):
        return self.__session


class MetricRepository(AbstractRepository):
    @property
    def table(self):
        return Metric.__table__

    def add(self, metric: Metric):
        super().add(metric)


class OperationRepository(AbstractRepository):
    def add(self, operation: Operation):
        super().add(operation)

    @property
    def table(self):
        return Operation.__table__


class LoadPlanRepository(AbstractRepository):
    @property
    def table(self):
        return LoadPlan.__table__


class ReportRepository(AbstractRepository):
    def add(self, report: LoadInfo):
        super().add(report)

    @property
    def table(self):
        return LoadInfo.__table__


class ReportOperationRepository(AbstractRepository):
    def add(self, report_operation: Report):
        super().add(report_operation)

    @property
    def table(self):
        return Report.__table__
