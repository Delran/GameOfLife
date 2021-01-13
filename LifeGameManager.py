# import curses
# from curses import wrapper

import random
import numpy as np

from LifeNode import LifeNode
# from SceneManager import SceneManager
# Scene viewer was build for Curses
# it is now deprecated and Qt handle
# the display
# from LifeGameSceneViewer import LifeGameSceneViewer

import defs
# import Utils


class LifeGameManager:

    __grid = []
    __length = 0
    __height = 0
    __area = 0
    __cyclePeriod = 0.2

    __sceneManager = None
    __sceneView = None

    __play = True

    anim = None

    def __init__(self):

        self.__length = defs.LENGTH
        self.__height = defs.HEIGHT
        self.__createGrid()

    def setSceneManager(self, sceneManager):
        self.__sceneManager = sceneManager

    def changeGameSize(self, length, height):
        self.__length = length
        self.__height = height
        self.__createGrid()

    def updateGrid(self):
        self.__cycle()

    def getGameDimensions(self):
        return self.__length, self.__height

    # Cycling, wait for a bit, compute and update every cells
    # in the game's grid
    def __cycle(self):
        self.__forEachNode(lambda i, j: self.__grid[i][j].compute())
        self.__forEachNode(lambda i, j: self.__grid[i][j].update())

    def flush(self):
        self.__forEachNode(lambda i, j: self.__grid[i][j].setAlive(False))

    def randomize(self):
        self.__forEachNode(lambda i, j: self.__grid[i][j].setAlive(random.randint(0, 100) > 80))

    # This function was added to provide support between the logical
    # grid and the matplotlib matrix,
    # Initial grid is an list of list of Nodes which cannot be converted
    # in an easy way to a numpy matrix, nor can it be changed to a numpy
    # matrix without significally altering the program structure.
    # So the logical grid is, for now, converted to a boolean numpy matrix
    # each generation.
    def getLogicalGrid(self):
        # Creating a zero matrix
        # Will be used as boolean, dtype to float for
        # easy handling of different colors for display
        matrix = np.zeros((self.__height, self.__length), dtype=float)

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

        return matrix

    # TODO : Next two function will be moved to SceneManager
    # Add scenes loaded to a temporary display grid
    def getLogicalGridWithScenes(self, select=True):
        matrix = self.getLogicalGrid()

        # Get the selected scene from the scene manager
        selected = self.__sceneManager.getCurrentScene()
        loadedScenes = self.__sceneManager.getLoadedScenes()
        for scene in loadedScenes:
            sceneMatrix = scene.getMatrix()
            x, y = scene.getXY()

            shape = np.shape(sceneMatrix)
            sceneH = shape[0]
            sceneL = shape[1]

            halfH = int(sceneH/2)
            halfL = int(sceneL/2)

            for i in range(sceneH):
                for j in range(sceneL):
                    value = sceneMatrix[i][j]
                    if not value:
                        continue
                    H = (i+y-halfH) % self.__height
                    L = (j+x-halfL) % self.__length
                    # If this is the selected item, change the value
                    # of the cell, this will change the color in which
                    # the cells are displayed
                    if select:
                        value = value/2 if selected == scene else value
                    matrix[H][L] = value
        return matrix

    def mergeScenes(self):
        # False means we don't want to change
        # the color of the selected scene
        matrix = self.getLogicalGridWithScenes(False)
        for i in range(self.__height):
            for j in range(self.__length):
                self.__grid[i][j].setAlive(matrix[i][j])

    def __createGrid(self):

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
                        # Pylama complains about whitespaces, couldn't care less
                        self.__grid[(i-1) % self.__height][(j)   % self.__length],  # North
                        self.__grid[(i-1) % self.__height][(j+1) % self.__length],  # NorthEast
                        self.__grid[(i)   % self.__height][(j+1) % self.__length],  # East
                        self.__grid[(i+1) % self.__height][(j+1) % self.__length],  # SouthEast
                        self.__grid[(i+1) % self.__height][(j)   % self.__length],  # South
                        self.__grid[(i+1) % self.__height][(j-1) % self.__length],  # SouthWest
                        self.__grid[(i)   % self.__height][(j-1) % self.__length],  # West
                        self.__grid[(i-1) % self.__height][(j-1) % self.__length],  # NorthWest
                    ])
        self.__forEachNode(linkLambda)

    # Pass i and j as params to given lambda
    # for each node in the grid
    def __forEachNode(self, fnLambda):
        for i in range(self.__height):
            for j in range(self.__length):
                fnLambda(i, j)

    '''
    ===============================================================
    ============ DEPRECATED SCENE ADDING FUNCTIONS ================
    ===============================================================
    '''
    # These functions are not part of the GUI and will only work
    # on .del legacy pattern files
    # There are kept only for debug purpose and will be removed
    # when no longer needed
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
                    node.setAlive(True)

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

    '''
    ===============================================================
    ================ END DEPRECATED FUNCTIONS =====================
    ===============================================================
    '''
