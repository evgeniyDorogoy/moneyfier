import asyncio

from helpers.time_helper import split_datetime_range_to_chunks
from transport.data_provider import MonobankDataProvider


class Monobank:
    def __init__(self, params, headers):
        self.account = params.get('account')[0]
        self.date_from = params.get('date_from')[0]
        self.date_to = params.get('date_to')[0]
        self.headers = headers

    async def get_statements_for_period(self):
        res = await asyncio.gather(
            *[
                MonobankDataProvider().get_statement(
                    date_from=int(dt_range[0].timestamp()),
                    date_to=int(dt_range[1].timestamp()),
                    account=self.account,
                    headers=self.headers,
                )
                for dt_range in split_datetime_range_to_chunks(self.date_from, self.date_to)
            ]
        )
        return res
