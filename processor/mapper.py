from datetime import datetime

from processor.parser import ExportFileParser


class CSVToDBMapper:

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
                'is_debet': float(el.get('amount').replace(',', '')) > 0
            }
            accumulator.append(result)
        return accumulator
