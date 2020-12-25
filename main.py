from LifeGameManager import LifeGameManager

length = 20
height = 20
sceneFolder = "Scenes"

gameOfLife = LifeGameManager(length, height, sceneFolder)

gameOfLife.addGlider(2, 2)
# gameOfLife.addScene("bigblinker", 10, 10)
# gameOfLife.addScene("block", 5, 5)
# gameOfLife.addScene("single", 5, 5)
# gameOfLife.addScene("single", 6, 5)
# gameOfLife.addScene("single", 7, 5)
# gameOfLife.addScene("column4", 10, 10)
# gameOfLife.addScene("column4", 13, 10)
# gameOfLife.addPulsar(2, 2)
gameOfLife.addPulsar(5, 5)

gameOfLife.start()
