from LifeGameManager import LifeGameManager

length = 20
height = 20
sceneFolder = "Scenes"

gameOfLife = LifeGameManager(length, height, sceneFolder)
# TODO : gameOfLife.start()
try:
    while True:
        gameOfLife.cycle()
except KeyboardInterrupt:
    print("Interupted game of life")
    pass
