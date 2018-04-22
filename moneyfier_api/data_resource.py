from sanic.response import json
from sanic.views import HTTPMethodView

from database.helper import synchronic_engine, asynchronic_engine
from database.models import Transactions
from processor.mapper import CSVToDBMapper
from sqlalchemy import select, func


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


class GetSumByCategories(HTTPMethodView):
    async def get(self, request):
        engine = await asynchronic_engine()
        accumulator = {'debet': {}, 'credit': {}}
        async with engine.acquire() as conn:
            query = select([
                Transactions.category,
                func.sum(Transactions.amount).label('amount'),
                Transactions.is_debet
            ]).group_by(
                Transactions.category,
                Transactions.is_debet
            ).order_by('amount')
            async for row in await conn.execute(query):
                if row[2]:
                    accumulator['debet'][row[0]] = row[1]
                else:
                    accumulator['credit'][row[0]] = row[1]
        return json(accumulator)
