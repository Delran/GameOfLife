from LifeGameManager import LifeGameManager


def main():

    length = 50
    height = 50
    sceneFolder = "Scenes"

    gameOfLife = LifeGameManager(length, height, sceneFolder)

    gameOfLife.addGlider(15, 15)
    # gameOfLife.addScene("blinker", 25, 25)
    # gameOfLife.addScene("bigblinker", 25, 25)
    # gameOfLife.addScene("block", 25, 25)
    # gameOfLife.addScene("single", 5, 6)
    # gameOfLife.addScene("single", 5, 5)
    # gameOfLife.addScene("single", 6, 5)
    # gameOfLife.addScene("single", 15, 8)
    # gameOfLife.addScene("single", 9, 10)
    # gameOfLife.addScene("single", 25, 15)
    # gameOfLife.addScene("single", 7, 5)
    # gameOfLife.addScene("column4", 25, 25)
    # gameOfLife.addScene("column4", 13, 10)
    # gameOfLife.addPulsar(2, 2)
    gameOfLife.addPulsar(25, 25)

    gameOfLife.start()


if __name__ == "__main__":
    # execute only if run as a script
    main()
