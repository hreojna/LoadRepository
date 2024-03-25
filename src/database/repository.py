import abc
import logging
from functools import singledispatchmethod
from typing import TypeVar, Type

from psycopg2 import errors
from sqlalchemy import exc, delete
from sqlalchemy.orm import Session, DeclarativeBase

from database.model import LoadInfo, Metric, Report, Operation, LoadPlan

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=DeclarativeBase)


class AbstractRepository(abc.ABC):
    base: Type[T]

    def __init__(self, session, base: Type[T]):
        self.__session: Session = session
        self.base = base

    def add(self, obj: T) -> T:
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

    def add_all(self, objs: list) -> list[T]:
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
        return self.session.execute(delete(self.base).where(self.base.c.id == obj))

    @delete.register
    def _delete(self, obj: T):
        self.session.execute(delete(self.base).where(self.base.c.id == obj))

    @property
    def session(self):
        return self.__session


class MetricRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session, Metric)


class OperationRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session, Operation)


class LoadPlanRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session, LoadPlan)


class LoadInfoRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session, LoadInfo)


class ReportRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session, Report)
