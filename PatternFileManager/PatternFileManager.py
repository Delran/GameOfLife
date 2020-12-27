import os.path
from os import path

from PatternFileManager.PatternReader.PlainFileReader import PlainFileReader
from PatternFileManager.PatternReader.RLEFileReader import RLEFileReader


# TODO: dictionnary of handled extentions with lambda constructors ?
class PatternFileManager:

    __patternFiles = []

    RLE = "rle"
    PLAIN = "plain"
    RLE_EXT = "." + RLE
    PLAIN_EXT = ".cells"

    def __init__(self, _path):

        # recursively get all files with handled extensions
        self.__exploreDir(_path)


    # Recursive function to explore all dirs inside given
    # as first parameter
    def __exploreDir(self, _path):
        files = os.listdir(_path)
        for file in files:
            fpath = _path + file
            if os.path.isdir(fpath):
                # Calls itself if the file is a directory
                self.__exploreDir(fpath+'/')
            else:
                # Getting lowered filename to avoid unexpected problems
                lower = fpath.lower()
                # Test if the filename ends with an handled extention
                if lower.endswith(self.RLE_EXT):
                    reader = RLEFileReader(fpath)
                elif lower.endswith(self.PLAIN_EXT):
                    reader = PlainFileReader(fpath)
                # If the extention is not recognized, do just continue
                else:
                    continue
                self.__patternFiles.append(reader)

    # @staticmethod
    # def readPatternFile(self, path):

    # @staticmethod
    # def readPatternFile(self, path):

    def readPlainText(self, ):
        pass
