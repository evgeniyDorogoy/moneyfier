from datetime import timedelta

import dateutil.parser


def split_datetime_range_to_chunks(datetime_from, datetime_to, chunk_size=2682000):

    if datetime_from > datetime_to:
        raise Exception(f'End of timerange {datetime_to} is behind of beginning of {datetime_from}')

    stop = datetime_to - timedelta(seconds=chunk_size)

    while datetime_from < stop:
        current = datetime_from + timedelta(seconds=chunk_size)
        yield datetime_from, current
        datetime_from += timedelta(seconds=chunk_size)

    yield datetime_from, datetime_to

def convert_datetime_string_to_datetime(datetime_string):
    return dateutil.parser.parse(datetime_string)

def convert_datatime_to_epoch(datatime_obj):
    return