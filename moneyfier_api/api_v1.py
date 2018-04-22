from moneyfier_api.app import app
from moneyfier_api.data_resource import GetSumByCategories, UpdateDatabaseWithLastData, GetAllRecords
from moneyfier_api.service_resource import CreateTables, DropTAbles
from moneyfier_api.transport_resource import DropboxResources

# service resources
app.add_route(CreateTables.as_view(), '/create-tables')
app.add_route(DropTAbles.as_view(), '/drop-tables')

# data provider resources
app.add_route(DropboxResources.as_view(), '/get-files')
app.add_route(UpdateDatabaseWithLastData.as_view(), '/update-with-last-data')

# data manipulation resources
app.add_route(GetAllRecords.as_view(), '/get-all-records')
app.add_route(GetSumByCategories.as_view(), '/get-sum-by-categories')
