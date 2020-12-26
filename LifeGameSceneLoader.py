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

    def saveScene(self, grid, sceneName):

        with open(self.__getFullPath(sceneName), 'w', newline='') as csvfile:
            sceneWriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
            for i in range(len(grid)):
                sceneWriter.writerow(grid[i])

    def __getFullPath(self, name):
        return self.__sceneFolderPath + name
