import inspect

import sys

from database import models
from config import DatabaseConfig
from collections import namedtuple


def make_db_url() -> str:
    db_conf = DatabaseConfig()
    return 'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'.format(db_user=db_conf.database_user,
                                                                             db_password=db_conf.database_password,
                                                                             db_host=db_conf.db_host,
                                                                             db_name=db_conf.database_name)


async def asynchronic_engine():
    from aiopg.sa import create_engine
    return await create_engine(make_db_url())


def synchronic_engine():
    from sqlalchemy import create_engine
    return create_engine(make_db_url())


def get_model_classes() -> list:
    Clsmember = namedtuple('Clsmember', ['cls_name', 'cls_def'])
    clsmembers = [Clsmember(member[0], member[1]) for member in inspect.getmembers(sys.modules[models.__name__],
                                                                                   inspect.isclass)]

    accumulator = []
    for el in clsmembers:
        if el.cls_name != models.Base.__name__ and issubclass(el.cls_def, models.Base):
            accumulator.append(el)
    return accumulator


def create_tables() -> list:
    engine = synchronic_engine()
    model_classes = get_model_classes()
    result = []
    for model in model_classes:
        model.cls_def.metadata.create_all(engine)
        result.append(model.cls_name)
    return result


def drop_tables() -> list:
    engine = synchronic_engine()
    model_classes = get_model_classes()
    result = []
    for model in model_classes:
        model.cls_def.metadata.drop_all(engine)
        result.append(model.cls_name)
    return result
