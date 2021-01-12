import sys
import matplotlib

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

from LifeGameManager import LifeGameManager
from SceneManager.SceneManager import SceneManager

import defs
import Utils

matplotlib.use('Qt5Agg')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setMinimumSize(500,500)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QHBoxLayout(self._main)

        self.__length = defs.LENGTH
        self.__height = defs.HEIGHT

        self.canvas = GameOfLifeCanvas(self, self.__length, self.__height)

        self.canvas.axes.axes.xaxis.set_visible(False)
        self.canvas.axes.axes.yaxis.set_visible(False)

        self.__sceneManager = SceneManager("Scenes")

        ''' Game of life creation, add scene here '''
        # Pass the scene manager to the game of life,
        # this is a temporary solution to allow addScene
        # function to continue to work with the new GUI
        self.__gameOfLife = LifeGameManager(self.__length, self.__height, self.__sceneManager)
        self.__gameOfLife.addGliderGun()
        self.__gameOfLife.addPulsar()

        matrix = self.__gameOfLife.getLogicalGrid()
        self.__img = self.canvas.axes.imshow(matrix, interpolation='None', cmap='viridis', aspect='equal')

        # TODO : Move all the boring layout thingy out of here

        # Start and pause buttons
        # TODO: replace the two buttons by one ?
        hbox = QtWidgets.QVBoxLayout()
        self.__startButton = QtWidgets.QPushButton("Start", self)
        self.__stopButton = QtWidgets.QPushButton("Pause", self)
        self.__stopButton.setEnabled(False)
        self.__startButton.setMaximumWidth(200)
        self.__stopButton.setMaximumWidth(200)
        self.__startButton.setMinimumHeight(30)
        self.__stopButton.setMinimumHeight(30)

        self.__startButton.clicked.connect(self.__launchAnimCallback)
        self.__stopButton.clicked.connect(self.__stopAnimCallback)
        hbox.addWidget(self.__startButton)
        hbox.addWidget(self.__stopButton)

        # Gui definition
        # Scene loader GUI
        sceneEditLayout = QtWidgets.QVBoxLayout()

        addSceneText = QtWidgets.QLabel("Choose a scene")
        labelLayout = QtWidgets.QVBoxLayout()
        labelLayout.addWidget(addSceneText)
        labelLayout.setAlignment(Qt.AlignCenter)
        sceneEditLayout.addLayout(labelLayout)

        # Scene combobox
        self.__sceneBox = QtWidgets.QComboBox(self)

        scenes = self.__sceneManager.getScenes()

        for scene in scenes:
            self.__sceneBox.addItem(scene.getName())

        sceneEditLayout.addWidget(self.__sceneBox)
        # Scene informations
        self.__sceneDesc = QtWidgets.QTextEdit(self)
        self.__sceneDesc.setReadOnly(True)
        placeholder = "No information\n"
        placeholder += "(This view will contains the description of the chosen scene)"
        self.__sceneDesc.setPlaceholderText(placeholder)
        self.__sceneDesc.setMaximumHeight(int(self.height()/2))
        sceneEditLayout.addWidget(self.__sceneDesc)

        # Text edits for coordinates
        coordLayout = QtWidgets.QHBoxLayout()
        self.__textEditX = QtWidgets.QLineEdit(self)
        self.__textEditX.setPlaceholderText("X coords")
        self.__textEditX.setValidator(QtGui.QIntValidator(0, self.__length, self));
        coordLayout.addWidget(self.__textEditX)
        self.__textEditY = QtWidgets.QLineEdit(self)
        self.__textEditY.setPlaceholderText("Y coords")
        self.__textEditY.setValidator(QtGui.QIntValidator(0, self.__height, self));
        coordLayout.addWidget(self.__textEditY)
        sceneEditLayout.addLayout(coordLayout)

        # Add scene button
        self.__sceneAddButton = QtWidgets.QPushButton("Add scene", self)
        self.__sceneAddButton.clicked.connect(self.__addSceneCallback)
        sceneEditLayout.addWidget(self.__sceneAddButton)

        # Loaded scene/pattern list
        self.__sceneList = QtWidgets.QListWidget(self)
        self.__sceneList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems);
        self.__sceneList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection);
        self.__sceneList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__sceneList.customContextMenuRequested[QtCore.QPoint].connect(self.__sceneListMenu)
        sceneEditLayout.addWidget(self.__sceneList)

        # Gui layout
        sceneEditLayout.setAlignment(Qt.AlignTop)
        layout.addLayout(sceneEditLayout)

        # Game layout
        hbox.setAlignment(Qt.AlignCenter)
        gameLayout = QtWidgets.QVBoxLayout()
        gameLayout.addLayout(hbox)
        gameLayout.addWidget(self.canvas)

        layout.addLayout(gameLayout)

    def __addSceneCallback(self):
        sceneId = self.__sceneBox.currentIndex()
        x,y = self.__getSceneXY()
        scene = self.__sceneManager.createScene(sceneId,x,y)
        Utils.printMatrix(scene.getMatrix())
        self.__sceneList.addItem(scene)
        self.__updateScenes()

    def __getSceneXY(self):

        x = 0
        xStr = self.__textEditX.text()
        if xStr:
            x = int(xStr)
            x = 0 if x < 0 or x > self.__length else x

        y = 0
        yStr = self.__textEditY.text()
        if yStr:
            y = int(yStr)
            y = 0 if y < 0 or y > self.__height else y

        return x,y

    # Empty function for signal tests
    def __doNothing(self):
        pass

    # Context menu function for right clikcs on
    # the loaded scene menu
    def __sceneListMenu(self):
        # Get global position of the mouse
        globalCoords = QtGui.QCursor.pos()
        # Get the position relative to the QListWidget
        relativeCoords = QWidget.mapFromGlobal(self.__sceneList, globalCoords)
        # Get the selected item
        selected = self.__sceneList.itemAt(relativeCoords);
        # If we clicked an item, show the menu at coords
        if selected:
            rightMenu = QtWidgets.QMenu("Choose")
            # Function removeWidgetItem doesn't seems to work in PyQt
            def fnFunc():
                item = self.__sceneList.takeItem(self.__sceneList.currentRow())
                self.__sceneManager.deleteScene(item)

            removeAction = QtWidgets.QAction("Delete", self, triggered = fnFunc)
            rightMenu.addAction(removeAction)

            addAction = QtWidgets.QAction("Rename", self, triggered = selected.rename) # define objects can be specified from the event
            rightMenu.addAction(addAction)
            rightMenu.exec_(globalCoords)

        # else, no item clicked, do nothing

    # With Scenes directly inheriting from
    # QListWidgetItem, they can be managed
    # as is directly from the Widget
    '''
    def __updateSceneList(self):
        scenes = self.__sceneManager.getLoadedScenes()
        self.__sceneList.clear()
        for scene in scenes:
            self.__sceneList.addItem(scene)
    '''

    # TODO : Merge theses two buttons into one
    # Callback for Play/Resume button
    def __launchAnimCallback(self):
        # Stat the matplotlib animation
        self.anim = FuncAnimation(self.canvas.figure, updateGrid, fargs=(self.__img, self.__gameOfLife), blit=True, interval=200)
        self.__stopButton.setEnabled(True)
        self.__startButton.setEnabled(False)

    # Callback for Pause button
    def __stopAnimCallback(self):
        self.__stopButton.setEnabled(False)
        self.__startButton.setEnabled(True)
        self.__startButton.setText("Resume")
        self.anim._stop()

    def __updateScenes(self):
        anim = FuncAnimation(self.canvas.figure, updateScenesDisplay, fargs=(self.__img), blit=True, repeat=False)


class GameOfLifeCanvas(FigureCanvas):
    def __init__(self, parent, width, height):
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)


def updateGrid(frame, img, game):
    game.updateGrid()
    matrix = game.getLogicalGrid()
    img.set_array(matrix)
    return img,

def updateScenesDisplay(frame, img, game):
    matrix = game.getLogicalGridWithScenes()
    img.set_array(matrix)
    return img,


if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    mainW = MainWindow()
    mainW.show()
    sys.exit(qApp.exec_())
