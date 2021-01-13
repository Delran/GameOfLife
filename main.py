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

        self.setMinimumSize(500, 500)

        self.__gameOfLife = LifeGameManager()
        self.__sceneManager = SceneManager("Scenes", self.__gameOfLife)
        self.__gameOfLife.setSceneManager(self.__sceneManager)

        self.__initGui()

    def __initGui(self):

        dimensions = self.__gameOfLife.getGameDimensions()
        length = dimensions[0]
        height = dimensions[1]

        self.canvas = GameOfLifeCanvas(self, length, height)

        self.canvas.axes.axes.xaxis.set_visible(False)
        self.canvas.axes.axes.yaxis.set_visible(False)

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
        self.__sceneBox = QtWidgets.QComboBox(self._main)

        scenes = self.__sceneManager.getScenes()

        for scene in scenes:
            self.__sceneBox.addItem(scene.getFileName())

        sceneEditLayout.addWidget(self.__sceneBox)
        # Scene informations
        self.__sceneDesc = QtWidgets.QTextEdit(self._main)
        self.__sceneDesc.setReadOnly(True)
        placeholder = "No information\n"
        placeholder += "(This view will contains the description of the chosen scene)"
        self.__sceneDesc.setPlaceholderText(placeholder)
        self.__sceneDesc.setMaximumHeight(int(self.height()/2))
        sceneEditLayout.addWidget(self.__sceneDesc)

        # Text edits for coordinates
        coordLayout = QtWidgets.QHBoxLayout()
        self.__textEditX = QtWidgets.QLineEdit(self._main)
        self.__textEditX.setPlaceholderText("X coords")
        maxLength = length-1
        self.__textEditX.setValidator(QtGui.QIntValidator(0, maxLength, self._main))
        xLabel = QtWidgets.QLabel("Max : "+str(maxLength))
        xLayout = QtWidgets.QVBoxLayout()
        xLayout.addWidget(xLabel)
        xLayout.addWidget(self.__textEditX)
        coordLayout.addLayout(xLayout)
        self.__textEditY = QtWidgets.QLineEdit(self._main)
        self.__textEditY.setPlaceholderText("Y coords")
        maxHeight = height-1
        self.__textEditY.setValidator(QtGui.QIntValidator(0, maxHeight, self._main))
        yLabel = QtWidgets.QLabel("Max : "+str(maxHeight))
        yLayout = QtWidgets.QVBoxLayout()
        yLayout.addWidget(yLabel)
        yLayout.addWidget(self.__textEditY)
        coordLayout.addLayout(yLayout)

        sceneEditLayout.addLayout(coordLayout)

        # Add scene button
        self.__sceneAddButton = QtWidgets.QPushButton("Add scene", self._main)
        self.__sceneAddButton.clicked.connect(self.__addSceneCallback)
        sceneEditLayout.addWidget(self.__sceneAddButton)

        # Loaded scene/pattern list
        self.__loadedSceneList = QtWidgets.QListWidget(self._main)
        self.__loadedSceneList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.__loadedSceneList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.__loadedSceneList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__loadedSceneList.customContextMenuRequested[QtCore.QPoint].connect(self.__loadedSceneListMenu)
        self.__loadedSceneList.installEventFilter(self)
        self.__loadedSceneList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        sceneEditLayout.addWidget(self.__loadedSceneList)

        # MergeSceneButton
        self.__sceneMergeButton = QtWidgets.QPushButton("Merge scene", self._main)
        self.__sceneMergeButton.clicked.connect(self.__mergeScenesCallback)
        sceneEditLayout.addWidget(self.__sceneMergeButton)

        # Gui layout
        sceneEditLayout.setAlignment(Qt.AlignTop)
        layout.addLayout(sceneEditLayout)

        # Game layout

        # Start and pause buttons
        # TODO: replace the two buttons by one ?
        animLayout = QtWidgets.QVBoxLayout()
        self.__animButton = QtWidgets.QPushButton("Start", self._main)
        self.__animButton.setFixedWidth(200)
        self.__animButton.setMinimumHeight(40)

        self.__animButton.clicked.connect(self.__animCallback)
        animLayout.addWidget(self.__animButton)

        self.__flushButton = QtWidgets.QPushButton("Flush", self._main)
        self.__flushButton.setFixedWidth(120)
        self.__flushButton.setMinimumHeight(30)
        self.__flushButton.clicked.connect(self.__confirmFlush)
        flushLayout = QtWidgets.QVBoxLayout()
        flushLayout.addWidget(self.__flushButton)
        flushLayout.setAlignment(Qt.AlignCenter)
        animLayout.setAlignment(Qt.AlignCenter)
        gameLayout = QtWidgets.QVBoxLayout()
        gameLayout.addLayout(flushLayout)
        gameLayout.addWidget(self.canvas)
        gameLayout.addLayout(animLayout)
        layout.addLayout(gameLayout)

        gameEditLayout = QtWidgets.QVBoxLayout()
        gameEditLayout.setAlignment(Qt.AlignCenter)
        sizeEditLayout = QtWidgets.QVBoxLayout()
        sizeValueLayout = QtWidgets.QHBoxLayout()
        sizeEditLabel = QtWidgets.QLabel("Resize game", self._main)
        self.__resizeLengthEdit = QtWidgets.QLineEdit(self._main)
        self.__resizeLengthEdit.setPlaceholderText("New length")
        self.__resizeLengthEdit.setValidator(QtGui.QIntValidator(self._main))
        self.__resizeHeightEdit = QtWidgets.QLineEdit(self._main)
        self.__resizeHeightEdit.setPlaceholderText("New height")
        self.__resizeHeightEdit.setValidator(QtGui.QIntValidator(self._main))
        self.__resizeButton = QtWidgets.QPushButton("Confirm resize", self._main)
        self.__resizeButton.setMinimumWidth(130)
        self.__resizeButton.clicked.connect(self.__resize)
        sizeValueLayout.addWidget(self.__resizeLengthEdit)
        sizeValueLayout.addWidget(self.__resizeHeightEdit)
        tmpLayout = QtWidgets.QVBoxLayout()
        tmpLayout.addWidget(sizeEditLabel)
        tmpLayout.setAlignment(Qt.AlignCenter)
        sizeEditLayout.addLayout(tmpLayout)
        sizeEditLayout.addLayout(sizeValueLayout)
        sizeEditLayout.addWidget(self.__resizeButton)
        gameEditLayout.addLayout(sizeEditLayout)
        layout.addLayout(gameEditLayout)

        matrix = self.__gameOfLife.getLogicalGrid()

        # DO NOT REMOVE, THIS IS A HACK
        # Setting the first pyplot figure with an
        # empty matrix result in animations functions
        # doing nothing, we set one cell alive on the
        # display grid to start the animations
        matrix[0][0]=True

        self.__img = self.canvas.axes.imshow(matrix, interpolation='None', cmap='viridis', aspect='equal')

        self.__sceneManager.setScenesWidget(self.__loadedSceneList)

        # Launch the scenes edit mode animation
        self.__startSceneUpdate()

    def __confirmFlush(self):
        confirm = QtWidgets.QMessageBox(self)
        qtStdYes = QtWidgets.QMessageBox.Yes
        confirm.setStandardButtons(qtStdYes |
            QtWidgets.QMessageBox.Cancel)
        confirm.setDefaultButton(qtStdYes)
        confirm.setText("Flushing Game of life's grid.")
        confirm.setInformativeText("The state of the grid will be lost")
        # Show the window before exec to get it's size
        confirm.show()
        halfWidth = int(confirm.width()/2)
        halfHeight = int(confirm.height()/2)
        half = QtCore.QPoint(halfWidth, halfHeight)
        confirm.move(QtGui.QCursor.pos() - half)
        ret = confirm.exec()
        if ret == qtStdYes:
            self.__gameOfLife.flush()

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
        x = -1
        xStr = self.__textEditX.text()
        if xStr:
            x = int(xStr)

        y = -1
        yStr = self.__textEditY.text()
        if yStr:
            y = int(yStr)

        return x, y

    def __resize(self):
        nLength = self.__resizeLengthEdit.text()
        nHeiht = self.__resizeHeightEdit.text()
        if nHeiht and nLength:
            self.__closeMainWidget()
            self.__gameOfLife.changeGameSize(int(nLength), int(nHeiht))
            self.__initGui()

    def __closeMainWidget(self):
        if self.__playing:
            self.__anim._stop()
        else:
            self.__editAnim._stop()
        self.canvas.close()
        self._main.close()

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

            setCoords = QtWidgets.QAction("Set coordinates",
                self, triggered=self.__sceneManager.setXYCurrent)
            removeAction = QtWidgets.QAction("Delete (Suppr)",
                self, triggered=self.__sceneManager.deleteCurrentScene)
            addAction = QtWidgets.QAction("Rename (F2)",
                self, triggered=self.__sceneManager.renameCurrentScene)
            rotateClock = QtWidgets.QAction("Rotate counter (A)",
                self, triggered=self.__sceneManager.rotateCounterCurrent)
            rotateCounter = QtWidgets.QAction("Rotate clockwise (E)",
                self, triggered=self.__sceneManager.rotateClockwiseCurrent)
            flipHor = QtWidgets.QAction("Flip horizontal (W)",
                self, triggered=self.__sceneManager.flipHorizontalCurrent)
            flipVer = QtWidgets.QAction("Flip vertical (C)",
                self, triggered=self.__sceneManager.flipVerticalCurrent)

            rightMenu.addAction(setCoords)
            rightMenu.addAction(removeAction)
            rightMenu.addAction(addAction)
            rightMenu.addAction(rotateClock)
            rightMenu.addAction(rotateCounter)
            rightMenu.addAction(flipHor)
            rightMenu.addAction(flipVer)

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
                elif key == Qt.Key_A or key == Qt.Key_E:
                    self.__sceneManager.rotateCurrent(key == Qt.Key_A)
                    return True
                elif key == Qt.Key_W or key == Qt.Key_C:
                    self.__sceneManager.flipCurrent(key == Qt.Key_W)
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

    __playing = False
    # TODO : Merge theses two buttons into one
    # Callback for Play/Resume button
    def __animCallback(self):
        # Stat the matplotlib animation
        if not self.__playing:
            self.__flushButton.setEnabled(False)
            self.__playing = True
            self.__animButton.setText("Pause")
            self.__anim = FuncAnimation(self.canvas.figure, updateGrid, fargs=(self.__img, self.__gameOfLife), blit=True, interval=200)
            self.__editAnim._stop()
        else :
            self.__flushButton.setEnabled(True)
            self.__playing = False
            self.__animButton.setText("Resume")
            self.__anim._stop()
            self.__startSceneUpdate()

    def __startSceneUpdate(self):
        self.__editAnim = FuncAnimation(self.canvas.figure, updateScenesDisplay, fargs=(self.__img, self.__gameOfLife), interval=50)

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
