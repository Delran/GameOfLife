from LifeGameManager import LifeGameManager

length = 20
height = 20
sceneFolder = "Scenes"

gameOfLife = LifeGameManager(length, height, sceneFolder)

gameOfLife.addGlider()
gameOfLife.addPulsar(5, 5)

gameOfLife.start()
