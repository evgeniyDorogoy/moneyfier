import datetime
import time

from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy import select, func, desc

from database.helper import synchronic_engine, asynchronic_engine
from database.models import Transactions
from processor.mapper import MonefyStatementMapper, MonobankStatementsMapper
from transport.data_provider import MonobankDataProvider


class UpdateDatabaseWithLastMonefyData(HTTPMethodView):
    def post(self, request):
        with synchronic_engine().connect() as conn:
            values_for_insert = MonefyStatementMapper().execute()
            conn.execute(Transactions.__table__.insert().values(values_for_insert))
            return json({'total_number_of_inserted_values': len(values_for_insert)})


class UpdateDatabaseWithLastMonobankData(HTTPMethodView):
    def get(self, request):

        date_to = datetime.datetime.fromtimestamp(time.time())
        date_from = date_to - datetime.timedelta(days=31)

        headers = {'X-Token': request.headers.get('X-Token')}

        statements = MonobankDataProvider().get_statement(
            date_from=int(date_from.timestamp()),
            date_to='',
            account=0,
            headers=headers)
        values_for_insert = MonobankStatementsMapper(statements, 0).execute()
        with synchronic_engine().connect() as conn:
            conn.execute(Transactions.__table__.insert().values(values_for_insert))
            return json({'total_number_of_inserted_values': len(values_for_insert)})

class GetAllRecords(HTTPMethodView):
    async def get(self, request):
        engine = await asynchronic_engine()
        accumulator = []
        async with engine.acquire() as conn:
            async for row in await conn.execute(Transactions.__table__.select()):
                accumulator.append(dict(row))
        return json(accumulator)


class GetSumByCategories(HTTPMethodView):
    async def get(self, request):
        engine = await asynchronic_engine()
        accumulator = {'debet': {}, 'credit': {}}
        async with engine.acquire() as conn:
            query = (
                select([Transactions.category, func.sum(Transactions.amount).label('amount'), Transactions.is_debet])
                .group_by(Transactions.category, Transactions.is_debet)
                .order_by(desc('amount'))
            )
            async for row in await conn.execute(query):
                if row[2]:
                    accumulator['debet'][row[0]] = row[1]
                else:
                    accumulator['credit'][row[0]] = row[1]
        return json(accumulator)
