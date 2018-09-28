import os


class DropBoxConfig:
    def __init__(self):
        self.acs_token = os.environ.get('ACS_TOKEN')
        self.src_folder = '/monefysource'
        self.dst_folder = os.path.join(os.path.dirname(__file__), 'downloads')
        self.db_user = os.environ.get('DB_USER')
        self.db_password = os.environ.get('DB_PASSWORD')
        self.db_name = os.environ.get('DB_NAME')

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


class TelegramConfig:
    def __init__(self):
        self.bt_tkn = os.environ.get('BOT_TOKEN')
        self.qry_interval = os.environ.get('QUERY_INTERVAL', 15)

    @property
    def bot_token(self):
        return self.bt_tkn

    @bot_token.setter
    def bot_token(self, bt_tkn):
        self.bt_tkn = bt_tkn

    @property
    def query_interval(self):
        return self.qry_interval

    @query_interval.setter
    def query_interval(self, qry_interval):
        self.qry_interval = qry_interval


class DatabaseConfig:
    def __init__(self):
        self.db_host = os.environ.get('DB_HOST', 'localhost')
        self.db_port = os.environ.get('DB_PORT', '5423')
        self.db_user = os.environ.get('DB_USER')
        self.db_password = os.environ.get('DB_PASSWORD')
        self.db_name = os.environ.get('DB_NAME', 'postgres')

    @property
    def database_host(self):
        return self.db_host

    @database_host.setter
    def database_host(self, db_host):
        self.db_host = db_host

    @property
    def database_port(self):
        return self.db_port

    @database_port.setter
    def database_port(self, db_port):
        self.db_port = db_port

    @property
    def database_user(self):
        return self.db_user

    @database_user.setter
    def database_user(self, db_user):
        self.db_user = db_user

    @property
    def database_password(self):
        return self.db_password

    @database_password.setter
    def database_password(self, db_password):
        self.db_password = db_password

    @property
    def database_name(self):
        return self.db_name

    @database_name.setter
    def database_name(self, db_name):
        self.db_name = db_name
