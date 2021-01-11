import os.path
from os import path

from PatternFileManager.PatternReader.PlainFileReader import PlainFileReader
from PatternFileManager.PatternReader.RLEFileReader import RLEFileReader
from PatternFileManager.PatternReader.LegacyFileReader import LegacyFileReader


# TODO: dictionnary of handled extentions with lambda constructors ?
class PatternFileManager:

    __patternFiles = []

    RLE_EXT = ".rle"
    PLAIN_EXT = ".cells"
    LEGACY_EXT = ".del"

    def __init__(self, _path):

        # recursively get all files with handled extensions
        self.__exploreDir(_path)

    # Recursive function to explore all dirs at given path
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
                # Passing len(self.__patternFiles) to use the size of the
                # pattern list as unique ID
                if lower.endswith(self.RLE_EXT):
                    reader = RLEFileReader(fpath, len(self.__patternFiles))
                elif lower.endswith(self.PLAIN_EXT):
                    reader = PlainFileReader(fpath, len(self.__patternFiles))
                elif lower.endswith(self.LEGACY_EXT):
                    reader = LegacyFileReader(fpath, len(self.__patternFiles))
                # If the extention is not recognized, do just continue
                else:
                    continue
                self.__patternFiles.append(reader)
