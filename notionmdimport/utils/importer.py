import os

from notion.client import NotionClient
from notion import block
from md2notion.upload import upload


class Notion():
    def __init__(self, token_v2, basepage):
        self.client = NotionClient(token_v2=token_v2)
        self.basepage = self.client.get_block(basepage)

        self.notion_folder_pages = dict()
        self.notion_folder_pages['/'] = self.basepage

    def add_page(self, basedir, wanted_dir):
        return self.notion_folder_pages[basedir].children.add_new(block.PageBlock, title=wanted_dir)

    def upload_wiki(self, path):
        if not os.path.exists(path):
            raise Exception(f'Wiki path {path} does not exist')

        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith(".md"):
                    # handle full paths
                    self.process_file(os.path.join(root[len(path):], f), path)

    def ensure_directory(self, dir_path):
        if dir_path in self.notion_folder_pages:
            return self.notion_folder_pages[dir_path]

        self.create_directory(dir_path)

    def create_directory(self, dir_path):
        dirs = [x for x in dir_path.split("/") if len(x) > 0]

        for x in range(len(dirs)):
            wanted_dir = dirs[x]
            # Start with '/', always
            basedir = '/' + '/'.join(dirs[:x])

            if os.path.join(basedir, wanted_dir) in self.notion_folder_pages:
                continue

            self.notion_folder_pages[os.path.join(basedir, wanted_dir)] = self.add_page(basedir, wanted_dir)

    def process_file(self, file_path, fs_path):
        print(f'\n\nNow processing file: {file_path}')
        if not file_path.startswith('/'):
            file_path = '/' + file_path

        basedir, filename = os.path.split(file_path)

        if basedir != '/':
            self.ensure_directory(basedir)

        local_path = os.path.join(fs_path, file_path[1:])
        self._upload_file(local_path, basedir)

    def _upload_file(self, local_path, basedir):
        with open(local_path, 'r', encoding='utf-8') as mdFile:
            # Remove .md
            title = os.path.split(local_path)[1][:-3]
            new_page = self.notion_folder_pages[basedir].children.add_new(block.PageBlock, title=title)
            upload(mdFile, new_page)
