from sanic.views import HTTPMethodView
from sanic.response import json
from transport.data_provider import DropBoxDataProvider


class DropboxResources(HTTPMethodView):
    def get(self, *args, **kwargs):
        files_got = DropBoxDataProvider().get_files()
        return json({'files_got': files_got})
