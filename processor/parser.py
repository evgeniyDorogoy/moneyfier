import os
import csv
import transliterate


class ExportFileParser:

    def __init__(self):
        self.target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')

    @staticmethod
    def translate(field):
        try:
            res = transliterate.translit(field, reversed=True)
        except transliterate.exceptions.LanguageDetectionError:
            res = field
        return res

    def get_filename_list(self):
        return sorted(os.listdir(self.target_path))

    def parse(self):
        with open(os.path.join(self.target_path, self.get_filename_list().pop())) as f:
            reader = csv.DictReader(f)
            accumulator = []
            for el in reader:
                el['description'] = self.translate(el.get('description'))
                accumulator.append(el)
            return accumulator
