import os.path
from os import path
import csv

from SceneManager.PatternReader.PlainFileReader import PlainFileReader
from SceneManager.PatternReader.RLEFileReader import RLEFileReader
from SceneManager.PatternReader.LegacyFileReader import LegacyFileReader
from SceneManager.Scene import Scene


# TODO: dictionnary of handled extentions with lambda constructors ?
class SceneManager:

    __patternFiles = []
    __loadedScenes = []

    RLE_EXT = ".rle"
    PLAIN_EXT = ".cells"
    LEGACY_EXT = ".del"

    __sceneFolderPath = ""

    def __init__(self, _path, length, height):
        if not path.isdir(_path):
            raise "Cannot find specified folder for scenes path"

        self.__length = length
        self.__height = height

        if _path[-1] != '/':
            _path += '/'
        self.__sceneFolderPath = _path
        self.__scenes = os.listdir(self.__sceneFolderPath)

        # recursively get all files with handled extensions
        self.__exploreDir(_path)

        self.__sceneGUID = 0

    # Recursive function to explore all dirs at given path
    def __exploreDir(self, _path):
        files = os.listdir(_path)
        for file in files:
            fpath = _path + file
            if os.path.isdir(fpath):
                # Calls itself if the file is a directory
                self.__exploreDir(fpath+'/')
            else:
                # Getting lowered filename to avoid unexpected problems
                lower = fpath.lower()
                # Test if the filename ends with an handled extention
                # Passing len(self.__patternFiles) to use the size of the
                # pattern list as unique ID
                if lower.endswith(self.RLE_EXT):
                    reader = RLEFileReader(fpath, len(self.__patternFiles))
                elif lower.endswith(self.PLAIN_EXT):
                    reader = PlainFileReader(fpath, len(self.__patternFiles))
                elif lower.endswith(self.LEGACY_EXT):
                    reader = LegacyFileReader(fpath, len(self.__patternFiles))
                # If the extention is not recognized, do just continue
                else:
                    continue
                self.__patternFiles.append(reader)

    def createSceneFromName(self, str):
        for i in range(len(self.__patternFiles)):
            pattern = self.__patternFiles[i]
            if pattern.getName() == str:
                self.createScene(i, 0, 0)
                break

    def createScene(self, id, x, y):
        pattern = self.__patternFiles[id]
        scene = Scene(self.__sceneGUID, pattern, x, y)
        self.__loadedScenes.append(scene)
        self.__sceneGUID += 1

        self.__sceneWidget.addItem(scene)
        self.__sceneWidget.setCurrentItem(scene)

    def deleteCurrentScene(self):
        item = self.__sceneWidget.takeItem(self.__sceneWidget.currentRow())
        self.__loadedScenes.remove(item)

    def renameCurrentScene(self):
        self.__sceneWidget.currentItem().rename()

    def moveCurrent(self, vec2):
        scene = self.__sceneWidget.currentItem()
        x, y = scene.getXY()
        x = (x + vec2[0]) % self.__length
        y = (y + vec2[1]) % self.__height
        scene.setXY(x, y)

    def clear(self):
        self.__sceneWidget.clear()
        self.__loadedScenes.clear()

    def getCurrentScene(self):
        return self.__sceneWidget.currentItem()

    def getLoadedScenes(self):
        return self.__loadedScenes

    # Need for a delete scene function ?

    def loadScene(self, name):
        if name not in self.__scenes:
            raise ValueError("No scene of given name : {}".format(name))
        scene = []
        with open(self.__getFullPath(name), encoding='UTF-8') as csvfile:
            sceneReader = csv.reader(csvfile)
            for row in sceneReader:
                scene.append(row)
        return scene

    def setScenesWidget(self, widget):
        self.__sceneWidget = widget

    def getScenes(self):
        return self.__patternFiles

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
