import abc
import logging

from psycopg2 import errors
from sqlalchemy import exc
from sqlalchemy.orm import Session

from database.model import ReportInfo, Metric, ReportOperation

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

    @property
    def session(self):
        return self.__session


class MetricRepository(AbstractRepository):
    def add(self, metric: Metric):
        super().add(metric)


class ReportRepository(AbstractRepository):
    def add(self, report: ReportInfo):
        super().add(report)


class ReportOperationRepository(AbstractRepository):
    def add(self, report_operation: ReportOperation):
        super().add(report_operation)
