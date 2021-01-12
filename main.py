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
# import Utils

matplotlib.use('Qt5Agg')

# TODO : Move to class file, avoid poluting main
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.__length = defs.LENGTH
        self.__height = defs.HEIGHT

        self.canvas = GameOfLifeCanvas(self, self.__length, self.__height)

        self.canvas.axes.axes.xaxis.set_visible(False)
        self.canvas.axes.axes.yaxis.set_visible(False)

        self.__sceneManager = SceneManager("Scenes", self.__length, self.__height)

        self.__initGui()

        ''' Game of life creation, add scene here '''
        # Pass the scene manager to the game of life,
        # this is a temporary solution to allow addScene
        # function to continue to work with the new GUI
        self.__sceneManager.setScenesWidget(self.__loadedSceneList)

        self.__gameOfLife = LifeGameManager(self.__length, self.__height, self.__sceneManager)

        self.__sceneManager.createSceneFromName("null")
        # self.__gameOfLife.addGliderGun()
        # self.__gameOfLife.addPulsar()

        matrix = self.__gameOfLife.getLogicalGrid()

        # DO NOT REMOVE, THIS IS A HACK
        # Setting the first pyplot figure with an
        # empty matrix result in animations functions
        # doing nothing, we set one cell alive on the
        # display grid to start the animations
        matrix[self.__height-1][self.__length-1]=True

        self.__img = self.canvas.axes.imshow(matrix, interpolation='None', cmap='viridis', aspect='equal')

        # Launch the scenes edit mode animation
        self.__startSceneUpdate()

    def __initGui(self):
        self.setMinimumSize(500, 500)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QHBoxLayout(self._main)

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
        maxLength = self.__length-1
        self.__textEditX.setValidator(QtGui.QIntValidator(0, maxLength, self))
        xLabel = QtWidgets.QLabel("Max : "+str(maxLength))
        xLayout = QtWidgets.QVBoxLayout()
        xLayout.addWidget(xLabel)
        xLayout.addWidget(self.__textEditX)
        coordLayout.addLayout(xLayout)
        self.__textEditY = QtWidgets.QLineEdit(self)
        self.__textEditY.setPlaceholderText("Y coords")
        maxHeight = self.__height-1
        self.__textEditY.setValidator(QtGui.QIntValidator(0, maxHeight, self))
        yLabel = QtWidgets.QLabel("Max : "+str(maxHeight))
        yLayout = QtWidgets.QVBoxLayout()
        yLayout.addWidget(yLabel)
        yLayout.addWidget(self.__textEditY)
        coordLayout.addLayout(yLayout)

        sceneEditLayout.addLayout(coordLayout)

        # Add scene button
        self.__sceneAddButton = QtWidgets.QPushButton("Add scene", self)
        self.__sceneAddButton.clicked.connect(self.__addSceneCallback)
        sceneEditLayout.addWidget(self.__sceneAddButton)

        # Loaded scene/pattern list
        self.__loadedSceneList = QtWidgets.QListWidget(self)
        self.__loadedSceneList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.__loadedSceneList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.__loadedSceneList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__loadedSceneList.customContextMenuRequested[QtCore.QPoint].connect(self.__loadedSceneListMenu)
        self.__loadedSceneList.installEventFilter(self)
        sceneEditLayout.addWidget(self.__loadedSceneList)

        # MergeSceneButton
        self.__sceneMergeButton = QtWidgets.QPushButton("Merge scene", self)
        self.__sceneMergeButton.clicked.connect(self.__mergeScenesCallback)
        sceneEditLayout.addWidget(self.__sceneMergeButton)

        # Gui layout
        sceneEditLayout.setAlignment(Qt.AlignTop)
        layout.addLayout(sceneEditLayout)

        # Game layout

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

        hbox.setAlignment(Qt.AlignCenter)
        gameLayout = QtWidgets.QVBoxLayout()
        gameLayout.addLayout(hbox)
        gameLayout.addWidget(self.canvas)
        layout.addLayout(gameLayout)

    def __addSceneCallback(self):
        sceneId = self.__sceneBox.currentIndex()
        x, y = self.__getSceneXY()
        self.__sceneManager.createScene(sceneId, x, y)
        # Set focus to the loaded list to use keyboard
        self.__loadedSceneList.setFocus()

    def __mergeScenesCallback(self):
        self.__gameOfLife.mergeScenes()
        self.__sceneManager.clear()

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

        return x, y

    # Context menu function for right clikcs on
    # the loaded scene menu
    def __loadedSceneListMenu(self):
        # Get global position of the mouse
        globalCoords = QtGui.QCursor.pos()
        # Get the position relative to the QListWidget
        relativeCoords = QWidget.mapFromGlobal(self.__loadedSceneList, globalCoords)
        # Get the selected item
        selected = self.__loadedSceneList.itemAt(relativeCoords)
        # If we clicked an item, show the menu at coords
        if selected:
            rightMenu = QtWidgets.QMenu("Choose")

            removeAction = QtWidgets.QAction("Delete (Suppr)", self, triggered=self.__sceneManager.deleteCurrentScene)
            rightMenu.addAction(removeAction)

            addAction = QtWidgets.QAction("Rename (F2)", self, triggered=self.__sceneManager.renameCurrentScene)
            rightMenu.addAction(addAction)
            rightMenu.exec_(globalCoords)

        # else, no item clicked, do nothing

    def eventFilter(self, object, event):
        # Filter event for the loaded scene widget
        if object == self.__loadedSceneList:
            if event.type() == QtCore.QEvent.KeyPress:
                key = event.key()
                if key == Qt.Key_Left or key == Qt.Key_Q:
                    self.__sceneManager.moveCurrent((-1,0))
                    return True
                elif key == Qt.Key_Right or key == Qt.Key_D:
                    self.__sceneManager.moveCurrent((1,0))
                    return True
                elif key == Qt.Key_Up or key == Qt.Key_Z:
                    self.__sceneManager.moveCurrent((0,-1))
                    return True
                elif key == Qt.Key_Down or key == Qt.Key_S:
                    self.__sceneManager.moveCurrent((0,1))
                    return True
                elif key == Qt.Key_F2:
                    self.__sceneManager.renameCurrentScene()
                    return True
                elif key == Qt.Key_Delete:
                    self.__sceneManager.deleteCurrentScene()
                    return True

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                return True

        return False

    # TODO : Merge theses two buttons into one
    # Callback for Play/Resume button
    def __launchAnimCallback(self):
        # Stat the matplotlib animation
        self.__editAnim._stop()
        self.__anim = FuncAnimation(self.canvas.figure, updateGrid, fargs=(self.__img, self.__gameOfLife), blit=True, interval=200)
        self.__stopButton.setEnabled(True)
        self.__startButton.setEnabled(False)

    # Callback for Pause button
    def __stopAnimCallback(self):
        self.__stopButton.setEnabled(False)
        self.__startButton.setEnabled(True)
        self.__startButton.setText("Resume")
        self.__anim._stop()
        self.__startSceneUpdate()

    def __startSceneUpdate(self):
        self.__editAnim = FuncAnimation(self.canvas.figure, updateScenesDisplay, fargs=(self.__img, self.__gameOfLife), interval=10, blit=True, repeat=False)

    # Empty function for Qt signals tests
    def __doNothing(self):
        pass


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
