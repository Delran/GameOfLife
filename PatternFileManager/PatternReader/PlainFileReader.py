from PatternFileManager.PatternReader.PatternFile import PatternFile


class PlainFileReader(PatternFile):

    def __init__(self, _path):
        super(PlainFileReader, self).__init__(_path)
