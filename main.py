import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper

from LifeGameManager import LifeGameManager


def main(stdscr):

    curses.curs_set(1)
    curses.mousemask(1)
    stdscr.keypad(1)

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

    # editwin = curses.newwin(height, length*2, 2, 2)
    # # rectangle(stdscr, 1, 1, height, length)
    # editwin.border()
    # stdscr.refresh()



    # box = Textbox(editwin)

    # # Let the user edit until Ctrl-G is struck.
    # box.edit()

 #if __name__ == "__main__":
 #    main()

wrapper(main)
