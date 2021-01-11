import sys
import matplotlib

from PyQt5 import QtWidgets

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

from LifeGameManager import LifeGameManager

import defs


matplotlib.use('Qt5Agg')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.anim = None
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        self.canvas = GameOfLifeCanvas(self, defs.LENGTH, defs.HEIGHT)
        layout.addWidget(self.canvas)

        self.canvas.axes.axes.xaxis.set_visible(False)
        self.canvas.axes.axes.yaxis.set_visible(False)

        self.__gameOfLife = LifeGameManager(defs.LENGTH, defs.HEIGHT, "Scenes")
        self.__gameOfLife.addGliderGun()
        self.__gameOfLife.addPulsar()
        matrix = self.__gameOfLife.getLogicalGrid()
        self.__img = self.canvas.axes.imshow(matrix, interpolation='None', cmap='viridis', aspect='equal')

        # Layout for Qt buttons
        hbox = QtWidgets.QHBoxLayout()
        self.__startButton = QtWidgets.QPushButton("Start", self)
        self.__stopButton = QtWidgets.QPushButton("Pause", self)
        self.__stopButton.setEnabled(False)
        self.__startButton.clicked.connect(self.__launchAnimCallback)
        self.__stopButton.clicked.connect(self.__stopAnimCallback)
        hbox.addWidget(self.__startButton)
        hbox.addWidget(self.__stopButton)
        layout.addLayout(hbox)

    def __launchAnimCallback(self):
        # Only animate if no animation
        if self.anim is None:
            # Stat the matplotlib animation
            self.anim = FuncAnimation(self.canvas.figure, updateGrid, fargs=(self.__img, self.__gameOfLife), blit=True, interval=200)
            self.__stopButton.setEnabled(True)

    def __stopAnimCallback(self):
        # Only stop if animation
        self.__stopButton.setEnabled(False)
        self.anim._stop()
        self.anim = None


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
