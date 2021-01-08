from PatternFileManager.PatternReader.PatternFile import PatternFile

import defs

class RLEFileReader(PatternFile):

    def __init__(self, _path, _id):
        super(RLEFileReader, self).__init__(_path, _id, 'o', 'b')

    def read(self):
        if self.pattern is None:
            self.pattern = []
            with open(self.getPath(), encoding='UTF-8') as patternFile:
                line = patternFile.readline()
                # Skipping the first batch of commented lines
                while line[0] == '#':
                    line = patternFile.readline()
                # First line without comment is the header
                #x=??,y=??,?????
                headerLine = line.replace(" ", "")
                headers = headerLine.split(',')
                length = int(headers[0][2:])
                height = int(headers[1][2:])

                for y in range(height):
                    row = []
                    for x in range(length):
                        row.append(defs.DEADCHAR)
                    self.pattern.append(row)

                # TODO: Parse the pattern's rules
                full = ""
                for line in patternFile:
                    if line[0] != '#':
                        full += line.strip()

                char = full[0]
                x = 0
                y = 0
                i = 0
                strInt = "0"
                # TODO: Must be redone, chosen algorithm proved to be
                # absolutely not appropriate for the task at hand
                while char != '!':
                    if char == '$':
                        toAdd = int(strInt)
                        toAdd = 1 if toAdd == 0 else toAdd
                        for j in range(toAdd):
                            y += 1
                            x = 0
                        strInt = "0"
                    elif char == self.aliveChar():
                        print(strInt)
                        toAdd = int(strInt)
                        toAdd = 1 if toAdd == 0 else toAdd
                        for j in range(toAdd):
                            print("y : {}, x :   {}".format(y,x))
                            self.pattern[y][x] = defs.ALIVECHAR
                            x+=1
                        strInt = "0"
                    elif char == self.deadChar():
                        print(strInt)
                        toAdd = int(strInt)
                        toAdd = 1 if toAdd == 0 else toAdd
                        for j in range(toAdd):
                            print("y : {}, x : {}".format(y,x))
                            self.pattern[y][x] = defs.DEADCHAR
                            x+=1
                        strInt = "0"
                    else:
                        strInt += char
                    i += 1
                    char = full[i]

                patternFile.close()

        return self.pattern
