import json
from datetime import datetime

import os

from processor.parser import ExportFileParser


class MonefyStatementMapper:
    def execute(self) -> list:
        data = ExportFileParser().parse()
        return self.map(data)

    @staticmethod
    def map(data) -> list:
        accumulator = []
        for el in data:

            result = {
                'transaction_date': datetime.strptime(el.get('date'), '%d/%m/%Y'),
                'account': el.get('account'),
                'category': el.get('category'),
                'amount': float(el.get('amount').lstrip('-').replace(',', '')),
                'currency': el.get('currency'),
                'converted_amount': float(el.get('converted amount').lstrip('-').replace(',', '')),
                'converted_currency': el.get('currency'),
                'description': el.get('description'),
                'is_debet': float(el.get('amount').replace(',', '')) > 0,
            }
            accumulator.append(result)
        return accumulator


class MonobankStatementsMapper:

    def __init__(self, statements, account):
        self.statements = statements
        self.account = account

    def execute(self) -> list:
        return self.map()

    def map(self) -> list:
        accumulator = []
        mcc_map_results = self._mcc_mapper()
        for el in self.statements:
            result = {
                'transaction_date': datetime.fromtimestamp(el.get('time')).date(),
                'account': self.account,
                'category': [i.get('irs_description') for i in mcc_map_results if int(i.get('mcc')) == el.get('mcc')][0],
                'amount': float(abs(el.get('amount'))) / 100,
                'currency': el.get('currencyCode'),
                'converted_amount': float(abs(el.get('amount'))) / 100,
                'converted_currency': el.get('currencyCode'),
                'description': el.get('description'),
                'is_debet': float(el.get('amount')) / 100 > 0,
            }
            accumulator.append(result)
        return accumulator

    def _mcc_mapper(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/mcc_codes.json')
        with open(path) as outfile:
            return json.load(outfile)
