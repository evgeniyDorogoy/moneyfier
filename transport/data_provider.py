import os
from collections import namedtuple
from logging import getLogger

import aiohttp
import dropbox
import requests

from config import DropBoxConfig
from transport.data_provider_exception import GetStatementException, MonobankDataProviderException

dpc = DropBoxConfig()

log = getLogger(__name__)


class DataProviderBase:
    smoke_url = None

    @staticmethod
    def make_get_request(url, headers=None) -> requests.models.Response:
        r = requests.get(url, headers=headers if headers else {})
        r.raise_for_status()
        return r

    def smoke(self) -> tuple:
        if not self.smoke_url:
            raise ValueError('You have to specify URL for smoke testing')
        result = self.make_get_request(self.smoke_url)
        return result.status_code, result.text

    def api_smoke(self):
        raise NotImplementedError


class DropBoxDataProvider(DataProviderBase):
    smoke_url = 'https://dropbox.com'

    def __init__(self):
        self.dbx = dropbox.Dropbox(dpc.access_token)

    def api_smoke(self) -> None:
        if not self.dbx.files_list_folder('').entries:
            raise Exception('There are no folders in your Dropbox account')

    def get_list_of_objects(self, path='', recursive=False) -> list:
        result = namedtuple('Result', ['filename', 'filepatch'])
        return [
            result(el.name, el.path_lower) for el in self.dbx.files_list_folder(path=path, recursive=recursive).entries
        ]

    def get_files(self) -> int:
        result_count = 0
        for file in self.get_list_of_objects(path=dpc.source_folder):
            self.dbx.files_download_to_file(os.path.join(dpc.destination_folder, file.filename), file.filepatch)
            result_count += 1
        return result_count


class MonobankDataProvider(DataProviderBase):
    smoke_url = 'https://api.monobank.ua'

    def api_smoke(self):
        result = self.make_get_request(url=self.smoke_url)
        if result.status_code != requests.codes.ok:
            raise MonobankDataProviderException('Monobank API is unreachable')

    async def get_statement(self, date_from, date_to, account, headers):
        url = f'{self.smoke_url}/personal/statement/{account}/{date_from}/{date_to}'
        log.info(f'Start getting data from {self.__class__} with next URL {url}')
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status != requests.codes.ok:
                    log.info(f'Response from {self.__class__} is: {response.status}, {response.reason}')
                    raise GetStatementException(
                        f'Statements for period from {date_from} to {date_to} for '
                        f'{account} are unreachable now: code: {response.status} message: {response.reason}'
                    )
                return await response.json()
