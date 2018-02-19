import os
import dropbox
import requests
from collections import namedtuple

from config import DropBoxConfig

dpc = DropBoxConfig()


class DataProviderBase:

    smoke_url = None

    @staticmethod
    def make_get_request(url) -> requests.models.Response:
        r = requests.get(url)
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
        return [result(el.name, el.path_lower) for el in self.dbx.files_list_folder(path=path, recursive=recursive).entries]

    def get_files(self) -> None:
        for file in self.get_list_of_objects(path=dpc.source_folder):
            self.dbx.files_download_to_file(os.path.join(dpc.destination_folder, file.filename), file.filepatch)
