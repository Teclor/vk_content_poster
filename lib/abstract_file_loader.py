from abc import ABCMeta, abstractmethod


class AbstractFileLoader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def move_to_posted(self, filename):
        pass

    @abstractmethod
    def get_files(self):
        pass
