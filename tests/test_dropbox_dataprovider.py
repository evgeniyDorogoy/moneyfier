from unittest.mock import patch, Mock, PropertyMock

import pytest

from transport.data_provider import DropBoxDataProvider


@patch('transport.data_provider.dropbox')
class TestDropboxDataProvider:

    @patch('transport.data_provider.DataProviderBase.make_get_request',
           new=Mock(return_value=Mock(status_code=200, text='Ok')))
    def test_smoke_positive(self, *args, **kwargs):
        result = DropBoxDataProvider().smoke()
        assert result[0] == 200
        assert result[1] == 'Ok'

    def test_smoke_missed_url(self, *args, **kwargs):
        with pytest.raises(ValueError):
            result = DropBoxDataProvider()
            result.smoke_url = None
            result.smoke()

    def test_api_smoke_positive(self, *args, **kwargs):
        result = DropBoxDataProvider()
        result.dbx = Mock()
        result.api_smoke()

    def test_api_smoke_negative(self, *args, **kwargs):
        with pytest.raises(Exception):
            result = DropBoxDataProvider()
            result.dbx.files_list_folder = Mock(return_value=Mock(entries=None))
            result.api_smoke()

    def test_get_list_of_object(self, *args, **kwargs):
        result = DropBoxDataProvider()

        dummy_file_object = Mock(path_lower='/monefysource/monefy.data.1-11-11.csv')

        # Following code are necessary for override 'name' attribute of 'Mock' object
        n = PropertyMock(return_value='Monefy.Data.1-11-11')
        type(dummy_file_object).name = n

        result.dbx.files_list_folder = Mock(return_value=Mock(entries=tuple([dummy_file_object])))

        list_of_objects = result.get_list_of_objects()

        assert isinstance(list_of_objects, list)
        assert isinstance(list_of_objects[0], tuple)
        assert list_of_objects[0].filename == 'Monefy.Data.1-11-11'
        assert list_of_objects[0].filepatch == '/monefysource/monefy.data.1-11-11.csv'
