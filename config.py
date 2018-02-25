import os


class DropBoxConfig:

    def __init__(self):
        self.acs_token = os.environ.get('ACS_TOKEN')
        self.src_folder = '/monefysource'
        self.dst_folder = os.path.join(os.path.dirname(__file__), 'downloads')

    @property
    def access_token(self):
        return self.acs_token

    @access_token.setter
    def access_token(self, acces_token):
        self.acs_token = acces_token

    @property
    def source_folder(self):
        return self.src_folder

    @source_folder.setter
    def source_folder(self, source_folder):
        self.src_folder = source_folder

    @property
    def destination_folder(self):
        return self.dst_folder

    @destination_folder.setter
    def destination_folder(self, destination_folder):
        self.dst_folder = destination_folder
