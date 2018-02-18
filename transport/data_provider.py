import os
import dropbox
import requests
from collections import namedtuple

from config import DropBoxConfig

dpc = DropBoxConfig()


class DataProviderBase:

    smoke_url = None

    def smoke(self) -> None:
        if not self.smoke_url:
            raise ValueError('You have to specify URL for smoke testing')

        r = requests.get(self.smoke_url)
        r.raise_for_status()

    def api_smoke(self):
        raise NotImplementedError


class DropBoxDataProvider(DataProviderBase):

    smoke_url = 'https://dropbox.com'

    def __init__(self):
        self.dbx = dropbox.Dropbox(dpc.access_token)

    def api_smoke(self) -> None:
        if not self.dbx.files_list_folder('').entries:
            raise Exception('There are no folders in your Dropbox account')

    def get_list_of_objects(self, path='', recursive=False) -> namedtuple:
        result = namedtuple('Result', ['filename', 'filepath'])

        return [result(el.name, el.path_lower) for el in self.dbx.files_list_folder(path=path, recursive=recursive).entries]

    def get_files(self) -> None:
        for file in self.get_list_of_objects(path=dpc.source_folder):
            self.dbx.files_download_to_file(os.path.join(dpc.destination_folder, file.filename), file.filepath)

if __name__ == '__main__':
    provider = DropBoxDataProvider()
    # print(provider.smoke())
    # print(provider.api_smoke())
    # print(provider.get_list_of_objects(path=dpc.source_folder))
    # print(provider.get_files())
