from abc import ABCMeta, abstractmethod


# Abstract class, inherited by all pattern readers
class PatternFile:

    __metaclass__ = ABCMeta

    __ALIVE_CHAR = None
    __DEAD_CHAR = None

    __path = None
    __name = ""

    def __init__(self, _path):
        self.__path = _path

    @abstractmethod
    def read(self):
        ...
