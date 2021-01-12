from abc import ABCMeta, abstractmethod


# Abstract class, inherited by all pattern readers
class PatternFile(metaclass=ABCMeta):

    __metaclass__ = ABCMeta

    __ALIVE_CHAR = None
    __DEAD_CHAR = None

    __path = None
    __name = ""

    pattern = None

    def __init__(self, _path, _id, _alive, _dead):
        self.__id = _id
        self.__path = _path
        self.__ALIVE_CHAR = _alive
        self.__DEAD_CHAR = _dead
        tokens = _path.split('/')
        tokens = tokens[-1].split('.')
        self.__name = tokens[0]

        self.__desc = ""

        self.length = 0
        self.height = 0

    def getPath(self):
        return self.__path

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def _setName(self, name):
        if name is not None:
            self.__name = name

    def _setDesc(self, desc):
        if desc is not None:
            self.__desc = desc

    def getDesc(self):
        return self.__desc

    def aliveChar(self):
        return self.__ALIVE_CHAR

    def deadChar(self):
        return self.__DEAD_CHAR

    @abstractmethod
    def read(self):
        ...
