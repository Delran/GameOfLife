from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QInputDialog

from SceneManager.PatternReader.PatternFile import PatternFile


# Inherit form QListWidgetItem to be used
# as Items in directly in the GUI
# This almost nullifies the need for a manager
class Scene(QListWidgetItem):

    def __init__(self, id, reader, name, x=0, y=0):
        QListWidgetItem.__init__(self, name)
        if not isinstance(reader, PatternFile):
            raise TypeError("Instanciating scene with a patern not derived from PatternFile")

        self.__id = id
        self.__x = x
        self.__y = y
        self.__reader = reader
        # Get grid from reader.
        self.__pattern = self.__reader.read()
        self.__name = name

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
