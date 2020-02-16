from marshmallow.exceptions import ValidationError
from sanic import response
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy import select, func, desc

from database.helper import synchronic_engine, asynchronic_engine
from database.models import Transactions
from moneyfier_api.forms import MonobankStatementsParamsSchema
from processor.mapper import MonefyStatementMapper
from services.monobank_service import Monobank


class UpdateDatabaseWithLastMonefyData(HTTPMethodView):
    def post(self, request):
        with synchronic_engine().connect() as conn:
            values_for_insert = MonefyStatementMapper().execute()
            conn.execute(Transactions.__table__.insert().values(values_for_insert))
            return json({'total_number_of_inserted_values': len(values_for_insert)})


class UpdateDatabaseWithLastMonobankData(HTTPMethodView):
    async def get(self, request):
        try:
            params = MonobankStatementsParamsSchema().load(dict(request.args))
        except ValidationError:
            return abort(403)
        headers = {'X-Token': request.headers.get('X-Token')}
        if not headers:
            return abort(422, 'You need to provide mandatory header: X-Token')
        await Monobank(params, headers).update_statements_for_period()
        return response.text('Statements updating process for Monobank data provider has been started')


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
