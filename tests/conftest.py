import pytest


@pytest.fixture(scope='function')
def mock_NotionClient(mocker):
    mocker.patch('notionmdimport.utils.importer.NotionClient')
