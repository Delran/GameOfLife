import numpy as np
import re

from SceneManager.PatternReader.PatternFile import PatternFile


class RLEFileReader(PatternFile):

    def __init__(self, _path, _id):
        super(RLEFileReader, self).__init__(_path, _id, 'o', 'b')

    # Get match and remove the regex from the matched string
    def searchAndRm(self, regex, string):
        tmp = re.search(regex + '.*', string)
        if tmp is not None:
            tmp = tmp.group(0)
            rmv = re.match(regex, tmp)
            return tmp[rmv.end():]
        return None

    # TODO : Make subfunctions
    def read(self):
        if self.pattern is None:
            self.pattern = []
            with open(self.getPath(), encoding='UTF-8') as patternFile:

                # First, get the whole text into a string
                full = ""
                for line in patternFile:
                    full += line

                # Get comments
                # '# N' is the name of the pattern
                self._setName(self.searchAndRm(r'#\s*N\s+', full))
                self._setDesc(self.searchAndRm(r'#\s*C\s+', full))
                # Get pattern dimensions and rules
                dimensions = re.search('\nx.*', full)
                dimensions = dimensions.group(0)
                dimensions = re.findall(r'\d+[^,]*', dimensions)

                self.length = int(dimensions[0])
                self.height = int(dimensions[1])
                self.pattern = np.zeros((self.height, self.length), dtype=float)

                # This regex match any rle <run_count><tag>
                runTagRe = r'\d*\s*[ob$]'
                # Getting the run length encoded data
                # match one or more runTagRe until !
                rle = re.search('(' + runTagRe + r'+\s*)+!', full)
                # remove whitespaces
                rle = "".join(rle.group(0).split())

                x = 0
                y = 0
                while rle[0] != '!':
                    # Match a rle <run_count><tag> group
                    match = re.match(runTagRe, rle)
                    rle = rle[match.end():]
                    match = match.group(0)
                    number = re.match(r'\d+', match)
                    tag = match[-1]
                    number = int(number.group(0)) if number is not None else 1
                    for i in range(0, number):
                        if tag == '$':
                            y += 1
                            x = 0
                        else:
                            self.pattern[y][x] = tag == 'o'
                            x += 1

                patternFile.close()

        return self.pattern
