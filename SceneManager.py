import os.path
from os import path
import csv

from PatternFileManager.PatternFileManager import PatternFileManager


# TODO: A Scene class must be created to handle
# scenes individually
class SceneManager:

    __sceneFolderPath = ""
    __scenes = []

    __patternManager = None

    def __init__(self, _path):
        if not path.isdir(_path):
            raise "Cannot find specified folder for scenes path"

        if _path[-1] != '/':
            _path += '/'
        self.__sceneFolderPath = _path
        self.__patternManager = PatternFileManager(self.__sceneFolderPath)
        self.__scenes = os.listdir(self.__sceneFolderPath)

    def loadScene(self, name):
        if name not in self.__scenes:
            raise "No scene of given name : {}".format(name)
        scene = []
        with open(self.__getFullPath(name), encoding='UTF-8') as csvfile:
            sceneReader = csv.reader(csvfile)
            for row in sceneReader:
                scene.append(row)
        return scene

    # TODO: following functions should be moved to a Scene class
    # Grids can easily be rotated and mirrored using
    # the same loop with inverted range
    # for range x: for reversed y    === 90° rotation clockwise
    # for reversed x: for range y    === 90° rotation counter clockwise
    # for reversed x: for reversed y === 180° rotation
    def __rotateScene(self, scene, rangeX, rangeY):
        rotatedScene = []
        for x in rangeX:
            row = []
            for y in rangeY:
                row.append(scene[y][x])
            rotatedScene.append(row)
        return rotatedScene

    def rotateSceneClockwise(self, scene):
        rangeX = range(len(scene[0]))
        # Using reversed(range()) as argument fo Y/Height
        # seems to be caused unexpected behavior
        # Using manually inverted range that print the same
        # result doesn't appear to have this problem
        rangeY = range(len(scene)-1, -1, -1)
        return self.__rotateScene(scene, rangeX, rangeY)

    def rotateSceneCounterClockwise(self, scene):
        rangeX = reversed(range(len(scene[0])))
        rangeY = range(len(scene))
        return self.__rotateScene(scene, rangeX, rangeY)

    def __flipScene(self, scene, rangeX, rangeY):
        flipedScene = []
        for y in rangeY:
            row = []
            for x in rangeX:
                row.append(scene[y][x])
            flipedScene.append(row)
        return flipedScene

    def flipHorizontal(self, scene):
        rangeX = range(len(scene[0])-1, -1, -1)
        rangeY = range(len(scene))
        return self.__flipScene(scene, rangeX, rangeY)

    def flipVertical(self, scene):
        rangeX = range(len(scene[0]))
        rangeY = range(len(scene)-1, -1, -1)
        return self.__flipScene(scene, rangeX, rangeY)

    def saveScene(self, grid, sceneName):
        with open(self.__getFullPath(sceneName), 'w', newline='') as csvfile:
            sceneWriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
            for i in range(len(grid)):
                sceneWriter.writerow(grid[i])

    def __getFullPath(self, name):
        return self.__sceneFolderPath + name
