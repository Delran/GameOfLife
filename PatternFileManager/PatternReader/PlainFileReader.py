from PatternFileManager.PatternReader.PatternFile import PatternFile

import defs


class PlainFileReader(PatternFile):

    def __init__(self, _path, _id):
        super(PlainFileReader, self).__init__(_path, _id, 'O', '.')

    # TODO: only read once, change function name ?
    def read(self):
        if self.pattern is None:
            self.pattern = []
            with open(self.getPath(), encoding='UTF-8') as patternFile:
                maxLength = 0
                for line in patternFile:
                    # TODO: handle 'special' comments
                    # like name or descritpion
                    if line[0] != '!':
                        # Get the length of the longest row
                        length = len(line)
                        maxLength = length if length > maxLength else maxLength
                        row = []
                        for char in line:
                            if char == self.aliveChar():
                                row.append(defs.ALIVECHAR)
                            elif char == self.deadChar():
                                row.append(defs.DEADCHAR)
                            else:
                                break
                        self.pattern.append(row)
                patternFile.close()

                # Iterating through the result grid and adding
                # dead cells to have the same length on each row
                for row in self.pattern:
                    for i in range(len(row), maxLength-1):
                        row.append(defs.DEADCHAR)

        return self.pattern
