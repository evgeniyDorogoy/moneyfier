from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView

from database.helper import (
    create_database,
    drop_database,
    create_tables,
    drop_tables,
    CreationFail,
    DropFail
)


class DatabaseProcessorBase(HTTPMethodView):

    @staticmethod
    def db_lifecycle_response_handler(lifecycle_function):
        existing_databases = []

        try:
            existing_databases = [el[0] for el in lifecycle_function()]
        except (CreationFail, DropFail) as e:
            abort(406, e)
        return json({'existing_databases': existing_databases})


class DatabaseProcessor(DatabaseProcessorBase):

    def post(self, *args):
        return self.db_lifecycle_response_handler(create_database)

    def delete(self, *args):
        return self.db_lifecycle_response_handler(drop_database)


class TableProcessor(HTTPMethodView):

    def post(self, request):
        created_tables = create_tables()
        return json({'created_tables': created_tables})

    def delete(self, request):
        dropped_tables = drop_tables()
        return json({'dropped_tables': dropped_tables})
