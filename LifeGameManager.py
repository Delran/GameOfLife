import time
import os

from LifeNode import LifeNode
from LifeGameSceneLoader import LifeGameSceneLoader


class LifeGameManager:

    __grid = []
    __displayGrid = []
    __length = 0
    __height = 0
    __area = 0
    __cyclePeriod = 0

    __sceneLoader = None

    def __init__(self, length, height, sceneDir, period=0.3):

        self.__sceneLoader = LifeGameSceneLoader(sceneDir)
        self.createGrid(length, height)
        # self.addPulsar(2, 2)
        # self.__sceneLoader.saveScene(self.__displayGrid, "testPulsar")

    def addScene(self, scene, x, y):
        sceneHeight = len(scene)
        sceneLength = len(scene[0])

        # TODO handle
        if x * y > self.__area:
            raise "Scene is too big for the grid dimensions"

        if x < 0 or y < 0:
            raise "Coordinates inferior to zero"

        if self.__length - (x + sceneLength) < 0 or self.__height - (y + sceneHeight) < 0:
            raise "Scene cannot fit at given coordinates"

        for i in range(sceneHeight):
            for j in range(sceneLength):
                node = self.__grid[i+y][j+x]
                if scene[i][j] == '0':
                    node.setAlive()

    def addPulsar(self, x=0, y=0):
        scene = self.__sceneLoader.loadScene("pulsar")
        self.addScene(scene, x, y)

    def addGlider(self, x=0, y=0):
        # making a standard glider
        scene = self.__sceneLoader.loadScene("glider")
        self.addScene(scene, x, y)

    def saveScene(self, name):
        self.__sceneLoader.saveScene(self.__displayGrid, name)

    # Pass i and j as params to given lambda
    # for each node in the grid
    def __forEachNode(self, func):
        for i in range(self.__height):
            for j in range(self.__length):
                func(i, j)

    # Will show n = cycles generations ( plus the initial state of the grid )
    def start(self, cycles=0):
        self.printGrid()
        infinite = cycles == 0
        try:
            while cycles > 0 or infinite:
                cycles -= 1
                self.__cycle()
        except KeyboardInterrupt:
            print("Interupted game of life")
            pass

    # Cycling, wait for a bit, compute and update every cells
    # in the game's grid
    def __cycle(self):
        time.sleep(0.3)

        self.__forEachNode(lambda i, j: self.__grid[i][j].compute())
        self.__forEachNode(lambda i, j: self.__grid[i][j].update())
        self.printGrid()

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
        # print("Acceccing node[{}][{}]".format(i-1 % self.__height, j   % self.__length))
        # print("Acceccing node[{}][{}]".format(i-1 % self.__height, j+1 % self.__length))
        # print("Acceccing node[{}][{}]".format(i   % self.__height, j+1 % self.__length))
        # print("Acceccing node[{}][{}]".format(i+1 % self.__height, j+1 % self.__length))
        # print("Acceccing node[{}][{}]".format(i+1 % self.__height, j   % self.__length))
        # print("Acceccing node[{}][{}]".format(i+1 % self.__height, j-1 % self.__length))
        # print("Acceccing node[{}][{}]".format(i   % self.__height, j-1 % self.__length))
        # print("Acceccing node[{}][{}]".format(i-1 % self.__height, j-1 % self.__length))

    # Todo: make a lambda that allows the use of __forEachNode
    def printGrid(self):
        # testLambda = lambda i, j : self.__grid[i][j].print()
        for i in range(self.__height):
            row = []
            for j in range(self.__height):
                node = self.__grid[i][j]
                char = '0' if node.isAlive() else ' '
                row.append(char)
            print(row)
            self.__displayGrid.append(row)
