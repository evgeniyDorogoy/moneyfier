import asyncio
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

    @staticmethod
    async def data_update(token, date_from, date_to):
        """
        Get data from Mono and upload to DB
        :param token: Monobank token
        :param date_from: Start date
        :param date_to: End date
        :return: None
        """

        statements = MonobankDataProvider().get_statement(
            date_from=int(date_from.timestamp()),
            date_to=int(date_to.timestamp()),
            account=0,
            headers={"x-token": token}
        )

        values_for_insert = MonobankStatementsMapper(statements, 0).execute()
        engine = await asynchronic_engine()
        async with engine.acquire() as conn:
            await conn.execute(Transactions.__table__.insert().values(values_for_insert))

    async def range_data_update(self, token, date_from, date_to):
        delta = datetime.timedelta(days=31)
        start = date_from
        end = start + delta if start + delta <= date_to else date_to
        while start < date_to:
            await self.data_update(token, start, end)
            start = end
            end = start + delta if start + delta <= date_to else date_to
            if start < date_to:
                await asyncio.sleep(90)

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

    def post(self, request):
        """
        That method will receive all data for period.
        :param request:
        :return: Response
        """
        token = request.headers.get('X-Token')
        data = request.json
        date_from = datetime.datetime.fromisoformat(data["date_from"])
        date_to = datetime.datetime.fromisoformat(data.get("date_to")) if data.get(
            "date_to") else datetime.datetime.fromtimestamp(time.time())
        asyncio.create_task(self.range_data_update(token, date_from, date_to))
        return json("Task accepted")


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
