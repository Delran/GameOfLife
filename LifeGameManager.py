import time
import os

from LifeNode import LifeNode

class LifeGameManager:

    __grid = []
    __length = 0
    __height = 0
    __cyclePeriod = 0

    def __init__( self, length, height, period = 0.3 ):

        self.createGrid( length, height )
        self.addPulsar()

    def addPulsar( self ):
        #making a pulsar
        #NorthWest
        self.__grid[5][6].setAlive()
        self.__grid[4][6].setAlive()
        self.__grid[3][6].setAlive()
        self.__grid[6][5].setAlive()
        self.__grid[6][4].setAlive()
        self.__grid[6][3].setAlive()

        self.__grid[3][1].setAlive()
        self.__grid[4][1].setAlive()
        self.__grid[5][1].setAlive()
        self.__grid[1][3].setAlive()
        self.__grid[1][4].setAlive()
        self.__grid[1][5].setAlive()
        #NorthEast
        self.__grid[5][8].setAlive()
        self.__grid[4][8].setAlive()
        self.__grid[3][8].setAlive()
        self.__grid[6][9].setAlive()
        self.__grid[6][10].setAlive()
        self.__grid[6][11].setAlive()

        self.__grid[3][13].setAlive()
        self.__grid[4][13].setAlive()
        self.__grid[5][13].setAlive()
        self.__grid[1][9].setAlive()
        self.__grid[1][10].setAlive()
        self.__grid[1][11].setAlive()
        #SouthWest
        self.__grid[8][5].setAlive()
        self.__grid[8][4].setAlive()
        self.__grid[8][3].setAlive()
        self.__grid[9][6].setAlive()
        self.__grid[10][6].setAlive()
        self.__grid[11][6].setAlive()

        self.__grid[13][3].setAlive()
        self.__grid[13][4].setAlive()
        self.__grid[13][5].setAlive()
        self.__grid[9][1].setAlive()
        self.__grid[10][1].setAlive()
        self.__grid[11][1].setAlive()
        #SouthEast
        self.__grid[9][8].setAlive()
        self.__grid[10][8].setAlive()
        self.__grid[11][8].setAlive()
        self.__grid[8][9].setAlive()
        self.__grid[8][10].setAlive()
        self.__grid[8][11].setAlive()

        self.__grid[9][13].setAlive()
        self.__grid[10][13].setAlive()
        self.__grid[11][13].setAlive()
        self.__grid[13][9].setAlive()
        self.__grid[13][10].setAlive()
        self.__grid[13][11].setAlive()



    def addGlider( self ):
        #making a standard glidder
        self.__grid[2][1].setAlive()
        self.__grid[2][2].setAlive()
        self.__grid[2][3].setAlive()
        self.__grid[1][3].setAlive()
        self.__grid[0][2].setAlive()


    #Pass i and j as params to given lambda
    #for each node in the grid
    def __forEachNode( self, func ):
        for i in range( self.__height ):
            for j in range( self.__length ):
                func( i, j )

    #Cycling, wait for a bit, compute and update every cells
    #in the game's grid
    def cycle( self ):
        time.sleep(0.3)

        self.__forEachNode( lambda i, j : self.__grid[i][j].compute() )
        self.__forEachNode( lambda i, j : self.__grid[i][j].update() )
        self.printGrid()

    def createGrid( self, length, height ):

        #Encapsulating length and height init
        #at grid creation, this is the only
        #time these params should be modified
        self.__length = length
        self.__height = height

        self.__grid = []
        for i in range( self.__height ):
            self.__grid.append( [] )
            row = self.__grid[i]
            for j in range( self.__length ):
                node = LifeNode()
                row.append( node )

        #Defining lambda here for more readability
        linkLambda = lambda i, j : self.__grid[i][j].link(
                    #Defining the array of link
                    [
                        self.__grid[(i-1)%self.__height][(j  )%self.__length], #North
                        self.__grid[(i-1)%self.__height][(j+1)%self.__length], #NorthEast
                        self.__grid[(i  )%self.__height][(j+1)%self.__length], #East
                        self.__grid[(i+1)%self.__height][(j+1)%self.__length], #SouthEast
                        self.__grid[(i+1)%self.__height][(j  )%self.__length], #South
                        self.__grid[(i+1)%self.__height][(j-1)%self.__length], #SouthWest
                        self.__grid[(i  )%self.__height][(j-1)%self.__length], #West
                        self.__grid[(i-1)%self.__height][(j-1)%self.__length], #NorthWest
                    ] )
        self.__forEachNode( linkLambda )
        #print("Acceccing node[{}][{}]".format(i-1%self.__height, j  %self.__length))
        #print("Acceccing node[{}][{}]".format(i-1%self.__height, j+1%self.__length))
        #print("Acceccing node[{}][{}]".format(i  %self.__height, j+1%self.__length))
        #print("Acceccing node[{}][{}]".format(i+1%self.__height, j+1%self.__length))
        #print("Acceccing node[{}][{}]".format(i+1%self.__height, j  %self.__length))
        #print("Acceccing node[{}][{}]".format(i+1%self.__height, j-1%self.__length))
        #print("Acceccing node[{}][{}]".format(i  %self.__height, j-1%self.__length))
        #print("Acceccing node[{}][{}]".format(i-1%self.__height, j-1%self.__length))

    #Todo: make a lambda that allows the use of __forEachNode
    def printGrid( self ):
        #testLambda = lambda i, j : self.__grid[i][j].print()
        for i in range( self.__height ):
            row = []
            for j in range( self.__height ):
                node = self.__grid[i][j]
                char = '0' if node.isAlive() else ' '
                row.append( char )
            print( row )


gameOfLife = LifeGameManager( 20, 20 )
gameOfLife.printGrid()
try:
    while True:
        gameOfLife.cycle()
except KeyboardInterrupt:
    print("Interupted game of life")
    pass
