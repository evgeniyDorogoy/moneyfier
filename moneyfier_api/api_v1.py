from moneyfier_api.app import app
from moneyfier_api.data_resource import GetSumByCategories, UpdateDatabaseWithLastMonefyData, GetAllRecords, UpdateDatabaseWithLastMonobankData
from moneyfier_api.service_resource import DatabaseProcessor, TableProcessor
from moneyfier_api.transport_resource import DropboxResources

# service resources
app.add_route(DatabaseProcessor.as_view(), '/database-lifecycle')
app.add_route(TableProcessor.as_view(), '/table-lifecycle')

# data provider resources
app.add_route(DropboxResources.as_view(), 'dropbox/get-data')
app.add_route(UpdateDatabaseWithLastMonefyData.as_view(), 'dropbox/update-with-latest-data')

app.add_route(UpdateDatabaseWithLastMonobankData.as_view(), 'monobank/update-with-latest-data')

# data manipulation resources
app.add_route(GetAllRecords.as_view(), '/get-records')
app.add_route(GetSumByCategories.as_view(), '/get-sum-by-categories')
