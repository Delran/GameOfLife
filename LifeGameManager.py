# import curses
# from curses import wrapper

import numpy as np

from LifeNode import LifeNode
# from SceneManager import SceneManager
# Scene viewer was build for Curses
# it is now deprecated and Qt handle
# the display
# from LifeGameSceneViewer import LifeGameSceneViewer

import defs
import Utils

class LifeGameManager:

    __grid = []
    __displayGrid = []
    __length = 0
    __height = 0
    __area = 0
    __cyclePeriod = 0.2

    __sceneManager = None
    __sceneView = None

    __play = True

    anim = None

    def __init__(self, length, height, sceneManager):

        self.__sceneManager = sceneManager
        self.__createGrid(length, height)
        # self.__sceneManager.saveScene(self.__displayGrid, "testPulsar")

    def updateGrid(self):
        self.__cycle()

    # Cycling, wait for a bit, compute and update every cells
    # in the game's grid
    def __cycle(self):
        self.__forEachNode(lambda i, j: self.__grid[i][j].compute())
        self.__forEachNode(lambda i, j: self.__grid[i][j].update())

    # This function was added to provide support between the logical
    # grid and the matplotlib matrix,
    # Initial grid is an list of list of Nodes which cannot be converted
    # in an easy way to a numpy matrix, nor can it be changed to a numpy
    # matrix without significally altering the program structure.
    # So the logical grid is, for now, converted to a boolean numpy matrix
    # each generation.
    def getLogicalGrid(self):
        # Creating a zero matrix of type bools
        matrix = np.zeros((self.__height, self.__length), dtype=bool)

        # Commented here is an lambda made that made use of
        # the __forEachNode node functions to assign each node
        # at the right coordinates
        # It used the np.put function as a work around for lambda
        # assignments in python.
        # The first of the two lambda was used to capture the local
        # matrix variable
        # fn = (lambda matrix: lambda i, j: np.put(matrix, (i*self.__height) + j, self.__grid[i][j].isAlive()))(matrix)
        # Results were inconsistent wich size changing grid.

        for i in range(self.__height):
            for j in range(self.__length):
                matrix[i][j] = self.__grid[i][j].isAlive()

        Utils.printMatrix(matrix)

        return matrix

    # Add scenes loaded to a temporary display grid
    def getLogicalGridWithScenes(self):
        matrix = self.getLogicalGrid()

        loadedScenes = self.__sceneManager.getLoadedScenes()
        for scene in loadedScenes:
            for x in scene:
                for y in scene:
                    pass

        return matrix

    def addScene(self, scene, x=0, y=0):

        # If a string was passed as argument,
        # we try to load it. (will be changed)
        if isinstance(scene, str):
            scene = self.__sceneManager.loadScene(scene)

        sceneHeight = len(scene)
        sceneLength = len(scene[0])

        if x * y > self.__area:
            raise ValueError("Scene is too big for the grid dimensions")

        if x < 0 or y < 0:
            raise ValueError("Coordinates inferior to zero")

        if self.__length - (x + sceneLength) < 0 or self.__height - (y + sceneHeight) < 0:
            raise ValueError("Scene cannot fit at given coordinates")

        for i in range(sceneHeight):
            for j in range(sceneLength):
                node = self.__grid[i+y][j+x]
                if scene[i][j] == defs.ALIVECHAR:
                    node.setAlive()

    def addPulsar(self, x=0, y=0):
        self.addScene("pulsar.del", x, y)

    def addBlock(self, x=0, y=0):
        self.addScene("block.del", x, y)

    def addGliderGun(self, x=0, y=0):
        scene = self.__sceneManager.loadScene("glidergun.del")
        # scene = self.__sceneManager.flipVertical(scene)
        # scene = self.__sceneManager.flipHorizontal(scene)
        self.addScene(scene, x, y)

    def addGlider(self, x=0, y=0):
        # making a standard glider
        self.addScene("glider.del", x, y)

    def saveScene(self, name):
        self.__sceneManager.saveScene(self.__displayGrid, name)

    def __createGrid(self, length, height):

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

        # ANNONYMOUS FUNCTION DEFINITION
        # Lambda function that will link each not to its neighbours
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

    # Pass i and j as params to given lambda
    # for each node in the grid
    def __forEachNode(self, fnLambda):
        for i in range(self.__height):
            for j in range(self.__length):
                fnLambda(i, j)

    def getFig(self):
        return self.__fig

    # Todo: make a lambda that allows the use of __forEachNode
    def printGrid(self):
        # testLambda = lambda i, j: self.__grid[i][j].print()
        for i in range(self.__height):
            row = []
            for j in range(self.__length):
                node = self.__grid[i][j]
                char = defs.ALIVECHAR if node.isAlive() else defs.DEADCHAR
                row.append(char)
            print(row)
            self.__displayGrid.append(row)
