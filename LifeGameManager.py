import time
from curses import wrapper

from LifeNode import LifeNode
from LifeGameSceneLoader import LifeGameSceneLoader
from LifeGameSceneViewer import LifeGameSceneViewer


class LifeGameManager:

    ALIVECHAR = '0'
    DEADCHAR = '-'

    __grid = []
    __displayGrid = []
    __length = 0
    __height = 0
    __area = 0
    __cyclePeriod = 0

    __sceneLoader = None
    __sceneView = None

    def __init__(self, length, height, sceneDir, period=0.3):

        self.__sceneLoader = LifeGameSceneLoader(sceneDir)
        self.createGrid(length, height)
        # self.__sceneLoader.saveScene(self.__displayGrid, "testPulsar")

    def addScene(self, scene, x=0, y=0):

        if isinstance(scene, str):
            scene = self.__sceneLoader.loadScene(scene)

        sceneHeight = len(scene)
        sceneLength = len(scene[0])

        if x * y > self.__area:
            raise "Scene is too big for the grid dimensions"

        if x < 0 or y < 0:
            raise "Coordinates inferior to zero"

        if self.__length - (x + sceneLength) < 0 or self.__height - (y + sceneHeight) < 0:
            raise "Scene cannot fit at given coordinates"

        for i in range(sceneHeight):
            for j in range(sceneLength):
                node = self.__grid[i+y][j+x]
                if scene[i][j] == self.ALIVECHAR:
                    node.setAlive()

    def addPulsar(self, x=0, y=0):
        self.addScene("pulsar", x, y)

    def addBlock(self, x=0, y=0):
        self.addScene("block", x, y)

    def addGliderGun(self, x=0, y=0):
        scene = self.__sceneLoader.loadScene("glidergun")
        # scene = self.__sceneLoader.flipVertical(scene)
        # scene = self.__sceneLoader.flipHorizontal(scene)
        self.addScene(scene, x, y)

    def addGlider(self, x=0, y=0):
        # making a standard glider
        self.addScene("glider", x, y)

    def saveScene(self, name):
        self.__sceneLoader.saveScene(self.__displayGrid, name)

    # Pass i and j as params to given lambda
    # for each node in the grid
    def __forEachNode(self, func):
        for i in range(self.__height):
            for j in range(self.__length):
                func(i, j)

    # Only encapsulate curses wrapper
    def start(self):
        wrapper(self.__loop)

    def __loop(self, screen):
        # Init scene view, will show the initial state of the grid
        self.__sceneView = LifeGameSceneViewer(screen, self.__grid)
        # Wait for user input to start
        self.__sceneView.showStartMessage()
        try:
            while True:
                # Cycle and update the logical grid
                self.__cycle()
                # Update the view
                self.__sceneView.update()
        except KeyboardInterrupt:
            pass

    # Cycling, wait for a bit, compute and update every cells
    # in the game's grid
    def __cycle(self):
        time.sleep(0.2)

        self.__forEachNode(lambda i, j: self.__grid[i][j].compute())
        self.__forEachNode(lambda i, j: self.__grid[i][j].update())

    def createGrid(self, length, height):

        # Encapsulating length and height init
        # at grid creation, this is the only
        # time these params should be modified
        self.__length = length
        self.__height = height

        self.__area = self.__length * self.__height

        self.__grid = []
        for i in range(self.__height):
            self.__grid.append([])
            row = self.__grid[i]
            for j in range(self.__length):
                node = LifeNode()
                row.append(node)

        # Defining lambda here for more readability
        def linkLambda(i, j): self.__grid[i][j].link(
                    # Defining the array of link
                    [
                        # This can surely be automated, think about it
                        self.__grid[(i-1) % self.__height][(j) % self.__length],    # North
                        self.__grid[(i-1) % self.__height][(j+1) % self.__length],  # NorthEast
                        self.__grid[(i) % self.__height][(j+1) % self.__length],    # East
                        self.__grid[(i+1) % self.__height][(j+1) % self.__length],  # SouthEast
                        self.__grid[(i+1) % self.__height][(j) % self.__length],    # South
                        self.__grid[(i+1) % self.__height][(j-1) % self.__length],  # SouthWest
                        self.__grid[(i) % self.__height][(j-1) % self.__length],    # West
                        self.__grid[(i-1) % self.__height][(j-1) % self.__length],  # NorthWest
                    ])
        self.__forEachNode(linkLambda)

    # Todo: make a lambda that allows the use of __forEachNode
    def printGrid(self):
        # testLambda = lambda i, j: self.__grid[i][j].print()
        for i in range(self.__height):
            row = []
            for j in range(self.__height):
                node = self.__grid[i][j]
                char = self.ALIVECHAR if node.isAlive() else self.DEADCHAR
                row.append(char)
            print(row)
            self.__displayGrid.append(row)
