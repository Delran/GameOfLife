from PatternFileManager.PatternReader.PatternFile import PatternFile
import csv

import defs


# Legacy reader for previous handmade format
class LegacyFileReader(PatternFile):

    def __init__(self, _path, _id):
        super(LegacyFileReader, self).__init__(_path, _id, defs.ALIVECHAR, defs.DEADCHAR)

    def read(self):
        if self.pattern is None:
            self.pattern = []
            with open(self.getPath(), encoding='UTF-8') as csvfile:
                sceneReader = csv.reader(csvfile)
                for row in sceneReader:
                    self.pattern.append(row)
            csvfile.close()
        return self.pattern
        # return self.pattern
