import numpy as np

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import *

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

        self.__reader = reader
        self.__pattern = self.__reader.read()
        self.__name = self.__reader.getName()
        QListWidgetItem.__init__(self, self.__name)

        self.__id = id

        dim = np.shape(self.__pattern)
        self.__x = x if x >= 0 else int(dim[1]/2)
        self.__y = y if y >= 0 else int(dim[0]/2)

    def getName(self):
        return self.__name

    def rename(self):
        self.__name, ok = QInputDialog.getText(None, "Renaming " + self.__name, "Enter new name")
        if ok:
            self.setText(self.__name)

    def askXY(self, length, height):
        dialog = QDialog()
        dialog.setWindowTitle("Set coordinates")
        dialogLayout = QVBoxLayout()
        coordsLayout = QHBoxLayout()
        xLayout = QVBoxLayout()
        yLayout = QVBoxLayout()
        labelX = QLabel("Max : " + str(length-1), dialog)
        editX = QLineEdit(dialog)
        editX.setText(str(self.__x))
        editX.setPlaceholderText("X coords")
        editX.setValidator(QtGui.QIntValidator(0, length-1, dialog))
        labelY = QLabel("Max : " + str(height-1), dialog)
        editY = QLineEdit(dialog)
        editY.setText(str(self.__y))
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
