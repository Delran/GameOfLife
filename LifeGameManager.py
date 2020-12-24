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


gameOfLife = LifeGameManager( 10, 10 )
gameOfLife.printGrid()

for i in range(10):
    gameOfLife.cycle()
