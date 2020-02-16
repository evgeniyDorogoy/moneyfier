import asyncio
import itertools

from database.helper import synchronic_engine
from database.models import Transactions
from helpers.time_helper import split_datetime_range_to_chunks
from processor.mapper import MonobankStatementsMapper
from transport.data_provider import MonobankDataProvider
from logging import getLogger

log = getLogger(__name__)


class Monobank:
    def __init__(self, params, headers):
        self.account = params.get('account')[0]
        self.date_from = params.get('date_from')[0]
        self.date_to = params.get('date_to')[0]
        self.headers = headers

    async def update_statements_for_period(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._update_statements_for_period())

    async def _update_statements_for_period(self):
        statements = await self._get_statements_for_period()
        statements_for_insert = MonobankStatementsMapper(list(itertools.chain.from_iterable(statements)), 0).execute()
        with synchronic_engine().connect() as conn:
            conn.execute(Transactions.__table__.insert().values(statements_for_insert))

    async def _get_statements_for_period(self, concurrently=False):
        if concurrently:
            return await self._get_statements_for_period_concurrently()
        return await self._get_statements_for_period_successively()

    async def _get_statements_for_period_concurrently(self):
        dt_ranges = split_datetime_range_to_chunks(self.date_from, self.date_to)
        res = await asyncio.gather(*[self._get_statement_for_period(dt_range) for dt_range in dt_ranges])
        return res

    async def _get_statements_for_period_successively(self):
        dt_ranges = split_datetime_range_to_chunks(self.date_from, self.date_to)
        result_accumulator = []
        for dt_range in dt_ranges:
            log.info(f'Start getting data for {dt_range} successively')
            result_accumulator.append(await self._get_statement_for_period(dt_range))
            await asyncio.sleep(60)
        return result_accumulator

    async def _get_statement_for_period(self, dt_range):
        return await MonobankDataProvider().get_statement(
            date_from=int(dt_range[0].timestamp()),
            date_to=int(dt_range[1].timestamp()),
            account=self.account,
            headers=self.headers,
        )
