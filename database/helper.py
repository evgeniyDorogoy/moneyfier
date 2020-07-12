import inspect
import sys
from collections import namedtuple
from logging import getLogger
from typing import Any, TypeVar

from config import DatabaseConfig
from database import models

log = getLogger(__name__)


def make_db_url(db_name: str) -> str:
    db_conf = DatabaseConfig()
    if db_name:
        db_conf.database_name = db_name
    db_url = 'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'.format(
        db_user=db_conf.database_user,
        db_password=db_conf.database_password,
        db_host=db_conf.db_host,
        db_name=db_conf.database_name,
    )
    log.debug(f'Composed database url is: {db_url}')
    return db_url


async def asynchronic_engine(db_name: str = None) -> Any:
    from aiopg.sa import create_engine
    return await create_engine(make_db_url(db_name))


def synchronic_engine(db_name: str = None) -> Any:
    """
    Main use case of this function - serve different database-related routines,
    such as database/tables creation, modification and deletion.

    warning:: make sure that isolation_level='AUTOCOMMIT' is suitable for your purposes

    """
    from sqlalchemy import create_engine

    return create_engine(make_db_url(db_name), isolation_level='AUTOCOMMIT')


def get_synchronic_connection(db_name: str = None) -> Any:
    engine = synchronic_engine(db_name)
    return engine.connect()


def create_database() -> Any:
    sql = 'CREATE DATABASE'
    return database_lifecycle_helper(sql, CreationFail)


def drop_database() -> Any:
    sql = 'DROP DATABASE'
    return database_lifecycle_helper(sql, DropFail)


def database_lifecycle_helper(sql: str, expn: TypeVar(Exception)):
    db_conf = DatabaseConfig()
    with get_synchronic_connection('postgres') as sc:
        try:
            sc.execute(sql + ' {}'.format(db_conf.db_name))
        except Exception as e:
            raise expn(e)
        return sc.execute('SELECT datname ' 'FROM pg_database ' 'WHERE datistemplate = false ')


def get_model_classes() -> list:
    Clsmember = namedtuple('Clsmember', ['cls_name', 'cls_def'])
    clsmembers = [
        Clsmember(member[0], member[1]) for member in inspect.getmembers(sys.modules[models.__name__], inspect.isclass)
    ]

    accumulator = []
    for el in clsmembers:
        if el.cls_name != models.Base.__name__ and issubclass(el.cls_def, models.Base):
            accumulator.append(el)
    return accumulator


def table_lifecycle_helper(lifecycle_attr: str) -> list:
    engine = synchronic_engine()
    model_classes = get_model_classes()
    result = []
    for model in model_classes:
        getattr(model.cls_def.metadata, lifecycle_attr)(engine)
        result.append(model.cls_name)
    return result


def create_tables() -> list:
    return table_lifecycle_helper('create_all')


def drop_tables() -> list:
    return table_lifecycle_helper('drop_all')


# custom errors definition
class CreationFail(Exception):
    pass


class DropFail(Exception):
    pass
