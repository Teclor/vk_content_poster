from pathlib import Path
import json


class Settings:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Settings, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True
            self.dir = str(Path(__file__).absolute().parent)
            self.file_path = self.dir + '/settings.json'
            self.settings = {}
            self.load()

    def load(self):
        with open(self.file_path, "r", encoding='UTF-8') as fp:
            if len(fp.readlines()) != 0:
                fp.seek(0)
                self.settings = json.load(fp)
            else:
                self.set_default()

    def get(self, name):
        return self.settings[name]

    def set(self, name, value):
        self.settings[name] = value

    def get_all(self):
        return self.settings

    def save(self):
        with open(self.file_path, "w+", encoding='UTF-8') as fp:
            json.dump(self.settings, fp)

    def __len__(self):
        return len(self.settings)

    def __del__(self):
        pass

    def set_default(self):
        pass
