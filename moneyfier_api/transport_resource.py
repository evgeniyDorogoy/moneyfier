import datetime

from sanic.views import HTTPMethodView
from sanic.response import json
from sqlalchemy.sql.functions import coalesce
from sqlalchemy import select

from database.helper import synchronic_engine, asynchronic_engine
from database.models import Transactions
from processor.mapper import CSVToDBMapper
from processor.parser import ExportFileParser
from transport.data_provider import DropBoxDataProvider


class DropboxResources(HTTPMethodView):
    def get(self, request):
        files_got = DropBoxDataProvider().get_files()
        return json({'files_got': files_got})


class UpdateDatabaseWithLastData(HTTPMethodView):
    def post(self, request):
        with synchronic_engine().connect() as conn:
            values_for_insert = CSVToDBMapper().execute()
            conn.execute(Transactions.__table__.insert().values(CSVToDBMapper().execute()))
            return json({'total_number_of_inserted_values': len(values_for_insert)})


class GetAllRecords(HTTPMethodView):
    async def get(self, request):
        engine = await asynchronic_engine()
        accumulator = []
        async with engine.acquire() as conn:
            async for row in await conn.execute(Transactions.__table__.select()):
                accumulator.append(dict(row))
        return json(accumulator)
