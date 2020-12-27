from abc import ABCMeta, abstractmethod


# Abstract class, inherited by all pattern readers
class PatternFile:

    __metaclass__ = ABCMeta

    __ALIVE_CHAR = None
    __DEAD_CHAR = None

    __path = None

    def __init(self, path):
        self.__path = path

    @abstractmethod
    def read(self):
        ...
