import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper

from LifeGameManager import LifeGameManager


def main(stdscr):

    curses.curs_set(1)
    stdscr.keypad(1)
    curses.mousemask(1)

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

    # gameOfLife.start()

    # editwin = curses.newwin(height, length*2, 2, 2)
    # # rectangle(stdscr, 1, 1, height, length)
    # editwin.border()
    # stdscr.refresh()
    pad = curses.newwin(height, length*2)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    #pad.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    # These loops fill the pad with letters; addch() is
    # explained in the next section
    while True:
        stdscr.addstr(0, 0, "Game of life by Delran: (hit Ctrl-C to end)")
        for y in range(height-1):
            for x in range(length*2-1):
                pad.addch(y, x, ' ', curses.color_pair(1) | curses.A_BOLD)

    # Displays a section of the pad in the middle of the screen.
    # (0,0) : coordinate of upper-left corner of pad area to display.
    # (5,5) : coordinate of upper-left corner of window area to be filled
    #         with pad content.
    # (20, 75) : coordinate of lower-right corner of window area to be
    #          : filled with pad content.

        #stdscr.addstr(0, 0, "UHDKUHQKUZD")
        event = stdscr.getch()
        if event == curses.KEY_MOUSE:
            pad.addstr(10, 0, "UHDKUHQKUZD")
        if event == ord("q"):
            pad.addstr(10, 0, "UHDKUHQKUZD")
        if event == ord("a"):
            pad.addstr(10, 0, "")

        stdscr.refresh()
        pad.refresh()

    # box = Textbox(editwin)

    # # Let the user edit until Ctrl-G is struck.
    # box.edit()

 #if __name__ == "__main__":
 #    main()

wrapper(main)
