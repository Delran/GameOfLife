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

    def rotateScene(self, scene, rLength, rHeight):
        rotatedScene = []
        for x in rLength:
            row = []
            for y in rHeight:
                row.append(scene[y][x])
            rotatedScene.append(row)
        return rotatedScene

    def rotateSceneClockwise(self, scene):
        # return self.rotateScene(scene, range(len(scene[0])), reversed(range(len(scene))))
        rotatedScene = []
        for x in range(len(scene[0])):
            row = []
            for y in reversed(range(len(scene))):
                row.append(scene[y][x])
            rotatedScene.append(row)
        return rotatedScene

    def rotateSceneCounterClockwise(self, scene):
        return self.rotateScene(scene, reversed(range(len(scene[0]))), range(len(scene)))
        # rotatedScene = []
        # for x in reversed(range(len(scene[0]))):
        #     row = []
        #     for y in range(len(scene)):
        #         row.append(scene[y][x])
        #     rotatedScene.append(row)
        # return rotatedScene

    def saveScene(self, grid, sceneName):

        with open(self.__getFullPath(sceneName), 'w', newline='') as csvfile:
            sceneWriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
            for i in range(len(grid)):
                sceneWriter.writerow(grid[i])

    def __getFullPath(self, name):
        return self.__sceneFolderPath + name
