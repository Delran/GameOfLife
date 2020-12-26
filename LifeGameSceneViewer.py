import curses


class LifeGameSceneViewer:

    __screen = None
    __grid = None
    __gridHeight = 0
    __gridLength = 0
    __rows = 0
    __cols = 0

    def __init__(self, screen, grid):

        # Init curses
        curses.curs_set(1)
        curses.mousemask(1)
        self.__screen = screen
        self.__screen.keypad(1)

        # Init curses color pairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

        # Init grid and sizes
        self.__grid = grid
        self.__gridHeight = len(grid)
        self.__gridLength = len(grid[0])

        self.update()

    # Wait for an input from the user
    def showStartMessage(self):
        str = "Press any key to start"
        strBeginX = int(self.__cols/2 - len(str)/2) + 1
        strBeginY = self.__beginY + self.__gridHeight + 2
        self.__screen.addstr(strBeginY, strBeginX, str, curses.A_BOLD)
        self.__screen.getch()

    def update(self):
        # Clear the view
        self.__screen.clear()

        # TODO: catch curses exception for terminal too small
        # for the given grid size

        # Get the size of the terminal
        self.__rows, self.__cols = self.__screen.getmaxyx()
        # Place the Game of life at the center of the terminal
        self.__beginY = int(self.__rows/2 - self.__gridHeight/2)
        self.__beginX = int(self.__cols/2 - self.__gridLength)

        win = curses.newwin(self.__gridHeight, self.__gridLength*2, self.__beginY, self.__beginX)

        title = "Game of life by Delran: (hit Ctrl-C to end)"
        strBegin = int(self.__cols/2 - len(title)/2) + 1
        self.__screen.addstr(self.__beginY-2, strBegin, title, curses.A_BOLD)

        # ! Using insch instead of addch as you cannot add
        #   anything at the end of a window in curses
        for y in reversed(range(self.__gridHeight)):
            for x in reversed(range(self.__gridLength)):
                # White cells are dead cells
                color = curses.color_pair(1)
                if self.__grid[y][x].isAlive():
                    color = curses.color_pair(2)
                # Column are small so we use two char by unit of length
                for i in range(2):
                    win.insch(y, 0, ' ', color | curses.A_BOLD)

        #self.__screen.addstr(0, 0, "UHDKUHQKUZD")
        #event = self.__screen.getch()
        #if event == curses.KEY_MOUSE:
        #    win.addstr(10, 0, "UHDKUHQKUZD")
        #if event == ord("q"):
        #    win.addstr(10, 0, "UHDKUHQKUZD")
        #if event == ord("a"):
        #    win.addstr(10, 0, "")

        self.__screen.noutrefresh()
        win.noutrefresh()

        curses.doupdate()
