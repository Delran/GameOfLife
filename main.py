import sys
import matplotlib

from PyQt5 import QtCore, QtWidgets

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

from LifeGameManager import LifeGameManager
from SceneManager.SceneManager import SceneManager

import defs


matplotlib.use('Qt5Agg')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setMinimumSize(500,500)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QHBoxLayout(self._main)

        self.canvas = GameOfLifeCanvas(self, defs.LENGTH, defs.HEIGHT)

        self.canvas.axes.axes.xaxis.set_visible(False)
        self.canvas.axes.axes.yaxis.set_visible(False)

        self.__sceneManager = SceneManager("Scenes")

        ''' Game of life creation, add scene here '''
        # Pass the scene manager to the game of life,
        # this is a temporary solution to allow addScene
        # function to continue to work with the new GUI
        self.__gameOfLife = LifeGameManager(defs.LENGTH, defs.HEIGHT, self.__sceneManager)
        self.__gameOfLife.addGliderGun()
        self.__gameOfLife.addPulsar()

        matrix = self.__gameOfLife.getLogicalGrid()
        self.__img = self.canvas.axes.imshow(matrix, interpolation='None', cmap='viridis', aspect='equal')

        # TODO : Move all the boring layout thingy out of here

        # Start and pause buttons
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
        self.__sceneBox = QtWidgets.QComboBox(self)

        scenes = self.__sceneManager.getScenes()

        for scene in scenes:
            self.__sceneBox.addItem(scene.getName())

        sceneEditLayout.addWidget(self.__sceneBox)
        # Scene informations
        self.__sceneDesc = QtWidgets.QTextEdit(self)
        self.__sceneDesc.setReadOnly(True)
        self.__sceneDesc.setPlaceholderText("No informations")
        self.__sceneDesc.setMaximumHeight(int(self.height()/2))
        sceneEditLayout.addWidget(self.__sceneDesc)

        # Text edits for coordinates
        coordLayout = QtWidgets.QHBoxLayout()
        self.__textEditX = QtWidgets.QLineEdit(self)
        self.__textEditX.setPlaceholderText("X coords")
        coordLayout.addWidget(self.__textEditX)
        self.__textEditY = QtWidgets.QLineEdit(self)
        self.__textEditY.setPlaceholderText("Y coords")
        coordLayout.addWidget(self.__textEditY)
        sceneEditLayout.addLayout(coordLayout)

        # Add scene button
        self.__sceneAdd = QtWidgets.QPushButton("Add scene", self)
        sceneEditLayout.addWidget(self.__sceneAdd)
        # Loaded scene/pattern list

        # Gui layout
        sceneEditLayout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(sceneEditLayout)

        # Game layout
        hbox.setAlignment(QtCore.Qt.AlignCenter)
        gameLayout = QtWidgets.QVBoxLayout()
        gameLayout.addLayout(hbox)
        gameLayout.addWidget(self.canvas)

        layout.addLayout(gameLayout)

    def __launchAnimCallback(self):
        # Stat the matplotlib animation
        self.anim = FuncAnimation(self.canvas.figure, updateGrid, fargs=(self.__img, self.__gameOfLife), blit=True, interval=200)
        self.__stopButton.setEnabled(True)
        self.__startButton.setEnabled(False)

    def __stopAnimCallback(self):
        self.__stopButton.setEnabled(False)
        self.__startButton.setEnabled(True)
        self.__startButton.setText("Resume")
        self.anim._stop()


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


if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    mainW = MainWindow()
    mainW.show()
    sys.exit(qApp.exec_())
