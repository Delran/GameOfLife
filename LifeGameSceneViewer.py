import curses
from curses.textpad import Textbox, rectangle


class LifeGameSceneViewer:

    __screen = None
    __grid = None
    __gridHeight = 0
    __gridLength = 0

    def __init__(self, screen, grid):
        curses.curs_set(1)
        curses.mousemask(1)
        self.__screen = screen
        self.__screen.keypad(1)

        self.__grid = grid
        self.__gridHeight = len(grid)
        self.__gridLength = len(grid[0])

    def update(self):

        self.__screen.clear()

        rows, cols = self.__screen.getmaxyx()
        beginY = int(rows/2 - self.__gridHeight/2)
        beginX = int(cols/2 - self.__gridLength)
        win = curses.newwin(self.__gridHeight, self.__gridLength*2, beginY, beginX)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

        #win.bkgd(curses.color_pair(1))

        title = "Game of life by Delran: (hit Ctrl-C to end)"
        strBegin = int(cols/2 - len(title)/2) + 1
        self.__screen.addstr(beginY-2, strBegin, title, curses.A_BOLD)

        # ! Using insch instead of addch as you cannot add
        # anything at the end of a window in curses
        for y in reversed(range(self.__gridHeight)):
            for x in reversed(range(self.__gridLength)):
                color = curses.color_pair(1)
                if self.__grid[y][x].isAlive():
                    color = curses.color_pair(2)
                win.insch(y, 0, ' ', color | curses.A_BOLD)
                win.insch(y, 0, ' ', color | curses.A_BOLD)

        #stdscr.addstr(0, 0, "UHDKUHQKUZD")
        #event = stdscr.getch()
        #if event == curses.KEY_MOUSE:
        #    win.addstr(10, 0, "UHDKUHQKUZD")
        #if event == ord("q"):
        #    win.addstr(10, 0, "UHDKUHQKUZD")
        #if event == ord("a"):
        #    win.addstr(10, 0, "")

        self.__screen.refresh()
        win.refresh()
