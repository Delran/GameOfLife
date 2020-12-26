import os.path
from os import path
import csv


class LifeGameSceneLoader:

    __sceneFolderPath = ""
    __scenes = []

    def __init__(self, _path):
        if not path.isdir(_path):
            raise "Cannot find specified folder for scenes path"

        if _path[-1] != '/':
            _path += '/'
        self.__sceneFolderPath = _path
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

    # Grids can easily be rotated and mirrored using
    # the same loop with inverted range
    # for range x: for reversed y    === 90° rotation clockwise
    # for reversed x: for range y    === 90° rotation counter clockwise
    # for reversed x: for reversed y === 180° rotation
    def rotateScene(self, scene, rangeX, rangeY):
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
        return self.rotateScene(scene, rangeX, rangeY)

    def rotateSceneCounterClockwise(self, scene):
        rangeX = reversed(range(len(scene[0])))
        rangeY = range(len(scene))
        return self.rotateScene(scene, rangeX, rangeY)

    def saveScene(self, grid, sceneName):
        with open(self.__getFullPath(sceneName), 'w', newline='') as csvfile:
            sceneWriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
            for i in range(len(grid)):
                sceneWriter.writerow(grid[i])

    def __getFullPath(self, name):
        return self.__sceneFolderPath + name
