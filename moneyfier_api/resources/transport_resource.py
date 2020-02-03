from sanic.response import json
from sanic.views import HTTPMethodView

from transport.data_provider import DropBoxDataProvider


class DropboxResources(HTTPMethodView):
    def get(self, request):
        files_got = DropBoxDataProvider().get_files()
        return json({'files_got': files_got})
