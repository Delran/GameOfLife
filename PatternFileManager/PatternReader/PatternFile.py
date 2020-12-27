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

    def getPath(self):
        return self.__path

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def aliveChar(self):
        return self.__ALIVE_CHAR

    def deadChar(self):
        return self.__DEAD_CHAR

    @abstractmethod
    def read(self):
        ...
