import os
import dropbox
import requests
from requests.exceptions import RequestException

from config import DropBoxConfig

dpc = DropBoxConfig()


class DataProviderBase:

    smoke_url = None

    def smoke(self) -> None:
        if not self.smoke_url:
            raise ValueError('You have to specify URL for smoke testing')

        r = requests.get(self.smoke_url)

        if not r.status_code == 200:
            raise RequestException('\n\nStatus code is {}\nStatus message is {}'.format(r.status_code, r.reason))

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
        return [{el.name: el.path_lower} for el in self.dbx.files_list_folder(path=path, recursive=recursive).entries]

    def get_files(self):
        for file in self.get_list_of_objects(path=dpc.source_folder):
            self.dbx.files_download_to_file(os.path.join(dpc.destination_folder,
                                            list(file.keys())[0]),
                                            list(file.values())[0])

if __name__ == '__main__':
    provider = DropBoxDataProvider()
    # print(provider.smoke())
    # print(provider.api_smoke())
    # print(provider.get_list_of_objects(path=dpc.source_folder))
    # print(provider.get_files())
