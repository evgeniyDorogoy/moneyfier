from datetime import timedelta
from logging import getLogger

import dateutil.parser

log = getLogger(__name__)


def split_datetime_range_to_chunks(datetime_from, datetime_to, chunk_size=2682000):

    log.info(f'Start converting timerange from {datetime_from} to {datetime_to} with chunk size chunk_size')

    if datetime_from > datetime_to:
        message = f'End of timerange {datetime_to} is behind of beginning of {datetime_from}'
        log.error(message)
        raise Exception(message)

    stop = datetime_to - timedelta(seconds=chunk_size)

    while datetime_from < stop:
        current = datetime_from + timedelta(seconds=chunk_size)
        log.info(f'Preparing timerange chunk from {datetime_from} to {current}')
        yield datetime_from, current
        datetime_from += timedelta(seconds=chunk_size)
    log.info(f'Preparing timerange chunk from {datetime_from} to {datetime_to}')
    yield datetime_from, datetime_to


def convert_datetime_string_to_datetime(datetime_string):
    return dateutil.parser.parse(datetime_string)


def convert_datatime_to_epoch(datatime_obj):
    return
