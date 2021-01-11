import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np


from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from LifeGameManager import LifeGameManager

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        length = 50
        height = 50
        sceneFolder = "Scenes"

        sc = GameOfLifeWindow(self, length, height, sceneFolder)

        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.setCentralWidget(sc)

        self.show()

class GameOfLifeWindow(FigureCanvasQTAgg):

    def __init__(self, parent, width, height, sceneFolder):

        gameOfLife = LifeGameManager(width, height, sceneFolder)

        gameOfLife.addGliderGun()
        # gameOfLife.addGlider(15, 15)
        # gameOfLife.addScene("blinker", 25, 25)
        # gameOfLife.addScene("bigblinker", 25, 25)
        # gameOfLife.addBlock(25, 25)
        # gameOfLife.addScene("single", 5, 6)
        # gameOfLife.addScene("single", 5, 5)
        # gameOfLife.addScene("single", 6, 5)
        # gameOfLife.addScene("single", 5, 4)
        # gameOfLife.addScene("single", 15, 8)
        # gameOfLife.addScene("single", 9, 10)
        # gameOfLife.addScene("single", 25, 15)
        # gameOfLife.addScene("single", 7, 5)
        # gameOfLife.addScene("column4", 25, 25)
        # gameOfLife.addScene("column4", 13, 10)
        # gameOfLife.addPulsar(2, 2)
        # gameOfLife.addPulsar(25, 25)

        grid = gameOfLife.getLogicalGrid()

        fig = Figure(figsize=(width, height))
        ax = fig.add_subplot()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        Z = np.matrix(grid)
        img = ax.imshow(Z, interpolation='None', cmap='viridis', aspect='equal')
        super(GameOfLifeWindow, self).__init__(fig)

        # gameOfLife.start()

if __name__ == "__main__":
    main()
