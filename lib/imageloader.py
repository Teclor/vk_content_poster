from pathlib import Path
import os
from lib.abstract_file_loader import AbstractFileLoader


class ImageLoader(AbstractFileLoader):

    def __init__(self, image_dir='memes', posted_dir='posted'):
        this_file_parent_dir = Path(__file__).parent.resolve()
        self.image_dir =  '{}/../{}'.format(this_file_parent_dir, image_dir)
        self.posted_dir = '{}/../{}'.format(this_file_parent_dir, posted_dir)
        self.file_names = []
        self.files = {}
        self.__create_if_not_exist()

    def get_names_sorted(self):
        for file in os.listdir(self.image_dir):
            self.file_names.append(file)
        self.file_names.sort()
        return self.file_names

    def move_to_posted(self, filename):
        os.rename('{}/{}'.format(self.image_dir, filename), '{}/{}'.format(self.posted_dir, filename))

    def __create_if_not_exist(self):
        if not Path(self.image_dir).is_dir():
            Path(self.image_dir).mkdir(parents=True, exist_ok=True)
        if not Path(self.posted_dir).is_dir():
            Path(self.posted_dir).mkdir(parents=True, exist_ok=True)

    def get_files(self):
        if not self.file_names:
            self.get_names_sorted()
        for name in self.file_names:
            self.files[name] = Path('{}/{}'.format(self.image_dir, name)).absolute().as_posix()
        return self.files
