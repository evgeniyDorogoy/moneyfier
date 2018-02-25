from moneyfier_api.app import app
from moneyfier_api.transport_resource import DropboxResources

app.add_route(DropboxResources.as_view(), '/get-all-files')
