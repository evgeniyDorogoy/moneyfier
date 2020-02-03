import datetime

from sqlalchemy import Column, String, Date, DateTime, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column('timestamp', DateTime, default=datetime.datetime.utcnow())
    transaction_date = Column('transaction_date', Date)
    account = Column('account', String)
    category = Column('category', String)
    amount = Column('amount', Float)
    currency = Column('currency', String)
    converted_amount = Column('converted_amount', Float)
    converted_currency = Column('converted_currency', String)
    description = Column('description', String)
    is_debet = Column('is_debet', Boolean)
