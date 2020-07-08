import pytest
from unittest import mock
from notionmdimport.utils import importer

# Replace with real value for smoke test
token_v2 = "my_super_secret"
basepage = "https://www.notion.so/wiki-57471782948f41248bb54ba86a6dd77d"


def test_init(mocker, mock_NotionClient):
    ctl = importer.Notion(token_v2, basepage)
    assert ctl.basepage is not None


def test_ensure_directory(mocker, mock_NotionClient):
    mock_create_directory = mocker.patch('notionmdimport.utils.importer.Notion.create_directory')

    ctl = importer.Notion(token_v2, basepage)

    # Shouldn't exist
    ctl.ensure_directory("/foo")
    assert mock_create_directory.call_args == mock.call('/foo')

    # Should exist (one level deep)
    mock_create_directory.reset_mock()
    ctl.notion_folder_pages['/foo'] = "some_value"
    ctl.ensure_directory("/foo")
    assert mock_create_directory.call_count == 0


def test_create_directory(mocker, mock_NotionClient):
    mock_add_page = mocker.patch('notionmdimport.utils.importer.Notion.add_page')

    ctl = importer.Notion(token_v2, basepage)

    # Starting fresh, new directory
    ctl.create_directory('/foo')
    assert mock_add_page.call_args == mock.call('/', 'foo')

    # Create a sub-directory
    mock_add_page.reset_mock()
    ctl.notion_folder_pages['/foo'] = "some_value"
    ctl.create_directory('/foo/bar')
    assert mock_add_page.call_args == mock.call('/foo', 'bar')

    # Assuming whole tree already exists
    mock_add_page.reset_mock()
    ctl.notion_folder_pages['/foo'] = "some_value"
    ctl.notion_folder_pages['/foo/bar'] = "some_value"
    ctl.create_directory('/foo/bar')
    assert mock_add_page.call_count == 0


def test_process_file(mocker, mock_NotionClient):
    mock_ensure_directory = mocker.patch('notionmdimport.utils.importer.Notion.ensure_directory')
    mocker.patch('notionmdimport.utils.importer.Notion._upload_file')

    ctl = importer.Notion(token_v2, basepage)

    # Adding file to basepath, no need to create directory
    ctl.process_file("/foo.md", "./")
    assert mock_ensure_directory.call_count == 0
    ctl.process_file("foo.md", "./")
    assert mock_ensure_directory.call_count == 0

    # Will create one directory
    mock_ensure_directory.reset_mock()
    ctl.process_file("/foo/bar.md", "./")
    assert mock_ensure_directory.call_args == mock.call('/foo')
    ctl.process_file("/foo/bar/new.md", "./")
    assert mock_ensure_directory.call_args == mock.call('/foo/bar')


def test_upload_wiki(mocker, mock_NotionClient):
    mock_add_page = mocker.patch('notionmdimport.utils.importer.Notion.add_page')

    ctl = importer.Notion(token_v2, basepage)

    # Non-existent wiki path
    with pytest.raises(Exception):
        importer.upload_wiki('./wiki')

    # Process all files
    ctl.upload_wiki('./testdata/wiki')
    assert mock.call('/', 'folder1') in mock_add_page.call_args_list
    assert mock.call('/', 'folder2') in mock_add_page.call_args_list
    assert mock.call('/folder1', 'folder11') in mock_add_page.call_args_list
    assert "/folder1" in ctl.notion_folder_pages
    assert "/folder2" in ctl.notion_folder_pages
    assert "/folder1/folder11" in ctl.notion_folder_pages


@pytest.mark.skip("this is a smoke test")
def test_smoke_upload_wiki(mocker):
    ctl = importer.Notion(token_v2, basepage)
    # Upload local wiki
    ctl.upload_wiki('./actual_wiki')
