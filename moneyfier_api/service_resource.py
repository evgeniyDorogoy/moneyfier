from sanic.response import json
from sanic.views import HTTPMethodView

from database.helper import create_tables, drop_tables


class CreateTables(HTTPMethodView):
    def post(self, request):
        created_tables = create_tables()
        return json({'created_tables': created_tables})


class DropTAbles(HTTPMethodView):
    def delete(self, request):
        dropped_tables = drop_tables()
        return json({'dropped_tables': dropped_tables})
