from sqlalchemy import select, func

from database.helper import asynchronic_engine
from database.models import Transactions


async def get_statistic():
    engine = await asynchronic_engine()
    accumulator = {'debet': {}, 'credit': {}}
    async with engine.acquire() as conn:
        query = (
            select([Transactions.category, func.sum(Transactions.amount).label('amount'), Transactions.is_debet])
                .group_by(Transactions.category, Transactions.is_debet)
                .order_by('amount')
        )
        async for row in await conn.execute(query):
            if row[2]:
                accumulator['debet'][row[0]] = row[1]
            else:
                accumulator['credit'][row[0]] = row[1]
    return accumulator