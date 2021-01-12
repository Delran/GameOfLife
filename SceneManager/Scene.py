import numpy as np

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QInputDialog

from SceneManager.PatternReader.PatternFile import PatternFile

import Utils
import defs

# Inherit form QListWidgetItem to be used
# as Items in directly in the GUI
# This almost nullifies the need for a manager
class Scene(QListWidgetItem):

    def __init__(self, id, reader, x=0, y=0):
        if not isinstance(reader, PatternFile):
            raise TypeError("Instanciating scene with a patern not derived from PatternFile")

        self.__id = id
        self.__x = x
        self.__y = y
        self.__reader = reader
        # Get grid from reader.
        self.__pattern = self.__reader.read()
        self.__name = self.__reader.getName()
        QListWidgetItem.__init__(self, self.__name)

    def getName(self):
        return self.__name

    def rename(self):
        self.__name, ok = QInputDialog.getText(None, "Renaming " + self.__name, "Enter new name")
        if ok:
            self.setText(self.__name)

    def getXY(self):
        return self.__x, self.__y

    def setXY(self, x, y):
        self.__x = x
        self.__y = y

    def getMatrix(self):
        return self.__pattern

    def getId(self):
        return self.__id

    # Grids can easily be rotated and mirrored using
    # the same loop with inverted range
    # for range x: for reversed y    === 90° rotation clockwise
    # for reversed x: for range y    === 90° rotation counter clockwise
    # for reversed x: for reversed y === 180° rotation
    def __rotateScene(self, rangeX, rangeY):
        rotatedScene = []
        for x in rangeX:
            row = []
            for y in rangeY:
                char = defs.ALIVECHAR if self.__pattern[y][x] else defs.DEADCHAR
                row.append(char)
            rotatedScene.append(row)
        self.__pattern = Utils.gridToMatrix(rotatedScene, len(rotatedScene), len(rotatedScene[0]))

    def rotateSceneClockwise(self):
        dim = np.shape(self.__pattern)
        rangeX = range(dim[1])
        # Using reversed(range()) as argument fo Y/Height
        # seems to be caused unexpected behavior
        # Using manually inverted range that print the same
        # result doesn't appear to have this problem
        rangeY = range(dim[0]-1, -1, -1)
        self.__rotateScene(rangeX, rangeY)

    def rotateSceneCounterClockwise(self):
        dim = np.shape(self.__pattern)
        rangeX = reversed(range(dim[1]))
        rangeY = range(dim[0])
        self.__rotateScene(rangeX, rangeY)

    def __flipScene(self, rangeX, rangeY):
        flipedScene = []
        for y in rangeY:
            row = []
            for x in rangeX:
                char = defs.ALIVECHAR if self.__pattern[y][x] else defs.DEADCHAR
                row.append(char)
            flipedScene.append(row)
        self.__pattern = Utils.gridToMatrix(flipedScene, len(flipedScene), len(flipedScene[0]))

    def flipHorizontal(self):
        dim = np.shape(self.__pattern)
        rangeX = range(dim[1]-1, -1, -1)
        rangeY = range(dim[0])
        self.__flipScene(rangeX, rangeY)

    def flipVertical(self):
        dim = np.shape(self.__pattern)
        rangeX = range(dim[1])
        rangeY = range(dim[0]-1, -1, -1)
        self.__flipScene(rangeX, rangeY)
