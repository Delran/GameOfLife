from LifeNode import LifeNode

class LifeGameManager:

    __grid = []
    __length = 0
    __height = 0

    def __init__( self, length, height ):

        self.createGrid( length, height )
        self.__grid[2][2].setAlive()
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

        for i in range( self.__height ):
            for j in range( self.__length ):
                node = self.__grid[i][j]
                #print("Acceccing node[{}][{}]".format(i-1%self.__height, j  %self.__length))
                #print("Acceccing node[{}][{}]".format(i-1%self.__height, j+1%self.__length))
                #print("Acceccing node[{}][{}]".format(i  %self.__height, j+1%self.__length))
                #print("Acceccing node[{}][{}]".format(i+1%self.__height, j+1%self.__length))
                #print("Acceccing node[{}][{}]".format(i+1%self.__height, j  %self.__length))
                #print("Acceccing node[{}][{}]".format(i+1%self.__height, j-1%self.__length))
                #print("Acceccing node[{}][{}]".format(i  %self.__height, j-1%self.__length))
                #print("Acceccing node[{}][{}]".format(i-1%self.__height, j-1%self.__length))
                linkArray = [
                                self.__grid[(i-1)%self.__height][(j  )%self.__length],
                                self.__grid[(i-1)%self.__height][(j+1)%self.__length],
                                self.__grid[(i  )%self.__height][(j+1)%self.__length],
                                self.__grid[(i+1)%self.__height][(j+1)%self.__length],
                                self.__grid[(i+1)%self.__height][(j  )%self.__length],
                                self.__grid[(i+1)%self.__height][(j-1)%self.__length],
                                self.__grid[(i  )%self.__height][(j-1)%self.__length],
                                self.__grid[(i-1)%self.__height][(j-1)%self.__length],
                            ]
                node.link( linkArray )


    def printGrid( self ):
        for i in range( self.__height ):
            row = []
            for j in range(self.__height):
                node = self.__grid[i][j]
                char = '0' if node.isAlive() else 'X'
                row.append( char )
            print( row )


test = LifeGameManager( 5, 5 )
