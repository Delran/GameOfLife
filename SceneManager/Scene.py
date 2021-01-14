from abc import ABCMeta, abstractmethod

import numpy as np

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import *

from SceneManager.PatternReader.PatternFile import PatternFile

import Utils
import defs


# Abstract class for two type of scenes
# All defined in the same file
class AbstractScene(QListWidgetItem):

    __metaclass__ = ABCMeta

    def __init__(self, id, x, y, pattern, name):
        self._id = id
        self._x = x
        self._y = y
        self._pattern = pattern
        self._name = name

        QListWidgetItem.__init__(self, self._name)

    def getName(self):
        return self._name

    def rename(self):
        self._name, ok = QInputDialog.getText(None, "Renaming " + self._name, "Enter new name")
        if ok:
            self.setText(self._name)

    @abstractmethod
    def clickEvent(self, x, y, button):
        ...

    @abstractmethod
    def createCopy(self, id):
        ...


    def askXY(self, length, height):
        dialog = QDialog()
        dialog.setWindowTitle("Set coordinates")
        dialogLayout = QVBoxLayout()
        coordsLayout = QHBoxLayout()
        xLayout = QVBoxLayout()
        yLayout = QVBoxLayout()
        labelX = QLabel("Max : " + str(length-1), dialog)
        editX = QLineEdit(dialog)
        editX.setText(str(self._x))
        editX.setPlaceholderText("X coords")
        editX.setValidator(QtGui.QIntValidator(0, length-1, dialog))
        labelY = QLabel("Max : " + str(height-1), dialog)
        editY = QLineEdit(dialog)
        editY.setText(str(self._y))
        editY.setPlaceholderText("Y coords")
        editY.setValidator(QtGui.QIntValidator(0, height-1, dialog))
        xLayout.addWidget(labelX)
        xLayout.addWidget(editX)
        yLayout.addWidget(labelY)
        yLayout.addWidget(editY)
        coordsLayout.addLayout(xLayout)
        coordsLayout.addLayout(yLayout)
        dialogLayout.addLayout(coordsLayout)
        confirmButton = QPushButton("Confirm", dialog)
        dialogLayout.addWidget(confirmButton)
        dialog.setLayout(dialogLayout)

        confirmButton.clicked.connect(dialog.close)
        # Show the dialog before excec to get it's size
        dialog.show()
        dWidth = int(dialog.width()/2)
        dHeight = int(dialog.height()/2)
        half = QPoint(dWidth, dHeight)
        dialog.move(QtGui.QCursor.pos() - half)
        dialog.exec_()

        strX = editX.text()
        strY = editY.text()
        X = int(strX) if strX else 0
        Y = int(strY) if strY else 0
        self.setXY(X, Y)

    def getXY(self):
        return self._x, self._y

    def setXY(self, x, y):
        self._x = x
        self._y = y

    def getMatrix(self):
        return self._pattern

    def getId(self):
        return self._id

    # Grids can easily be rotated and mirrored using
    # the same loop with inverted range
    # for range x: for reversed y    === 90° rotation clockwise
    # for reversed x: for range y    === 90° rotation counter clockwise
    # for reversed x: for reversed y === 180° rotation
    def _rotateScene(self, rangeX, rangeY):
        rotatedScene = []
        for x in rangeX:
            row = []
            for y in rangeY:
                char = defs.ALIVECHAR if self._pattern[y][x] else defs.DEADCHAR
                row.append(char)
            rotatedScene.append(row)
        self._pattern = Utils.gridToMatrix(rotatedScene, len(rotatedScene), len(rotatedScene[0]))

    def rotateSceneClockwise(self):
        dim = np.shape(self._pattern)
        rangeX = range(dim[1])
        # Using reversed(range()) as argument fo Y/Height
        # seems to be caused unexpected behavior
        # Using manually inverted range that print the same
        # result doesn't appear to have this problem
        rangeY = range(dim[0]-1, -1, -1)
        self._rotateScene(rangeX, rangeY)

    def rotateSceneCounterClockwise(self):
        dim = np.shape(self._pattern)
        rangeX = reversed(range(dim[1]))
        rangeY = range(dim[0])
        self._rotateScene(rangeX, rangeY)

    def _flipScene(self, rangeX, rangeY):
        flipedScene = []
        for y in rangeY:
            row = []
            for x in rangeX:
                char = defs.ALIVECHAR if self._pattern[y][x] else defs.DEADCHAR
                row.append(char)
            flipedScene.append(row)
        self._pattern = Utils.gridToMatrix(flipedScene, len(flipedScene), len(flipedScene[0]))

    def flipHorizontal(self):
        dim = np.shape(self._pattern)
        rangeX = range(dim[1]-1, -1, -1)
        rangeY = range(dim[0])
        self._flipScene(rangeX, rangeY)

    def flipVertical(self):
        dim = np.shape(self._pattern)
        rangeX = range(dim[1])
        rangeY = range(dim[0]-1, -1, -1)
        self._flipScene(rangeX, rangeY)


class PaintScene(AbstractScene):
    def __init__(self, id, pattern, name, dimensions, x=0, y=0):
        self.__dimensions = dimensions
        self.__length = dimensions[1]
        self.__height = dimensions[0]
        super(PaintScene, self).__init__(id, x, y, pattern, name)

    def createCopy(self, id):
        return Scene(id, self._pattern, self._name, self.__dimensions, self._x, self._y)

    def clickEvent(self, x, y, button):
        y = y - int(self.__height/2)
        x = x - int(self.__length/2)
        if button == 1:
            self._pattern[y][x] = True
        if button == 2:
            self._pattern[y][x] = False


# Inherit form QListWidgetItem to be used
# as Items in directly in the GUI
# This almost nullifies the need for a manager
class Scene(AbstractScene):

    def __init__(self, id, reader, x=0, y=0, pattern = None):
        if not isinstance(reader, PatternFile):
            raise TypeError("Instanciating scene with a patern not derived from PatternFile")

        self.__reader = reader
        if pattern is None:
            pattern = self.__reader.read()

        name = self.__reader.getName()

        dim = np.shape(pattern)
        x = x if x >= 0 else int(dim[1]/2)
        y = y if y >= 0 else int(dim[0]/2)
        super(Scene, self).__init__(id, x, y, pattern, name)

    def createCopy(self, id):
        return Scene(id, self.__reader, self._x, self._y, self._pattern)

    def clickEvent(self, x, y, button):
        if button == 1:
            self._x = x
            self._y = y
