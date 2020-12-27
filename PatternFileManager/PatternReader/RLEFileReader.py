from PatternFileManager.PatternReader.PatternFile import PatternFile


class RLEFileReader(PatternFile):

    def __init__(self, _path, _id):
        super(RLEFileReader, self).__init__(_path, _id, 'o', 'b')

    def read(self):
        if self.pattern is None:
            with open(self.getPath(), encoding='UTF-8') as patternFile:
                for line in patternFile:
                    print(line)

                patternFile.close()
        # return self.pattern
