

class LifeNode:

    #Links are clockwise starting at 0 o'clock
    # links[0] = North
    # links[1] = NorthEast
    # links[2] = East
    # links[3] = SouthEast
    # links[4] = South
    # links[5] = SouthWest
    # links[6] = West
    # links[7] = NorthWest
    __links = []
    __alive = False

    def __init__( self ):
        #                N     NE    E     SE    S     SW    W     NW
        self.__links = [ None, None, None, None, None, None, None, None ]

    def __assertIsNode( self, node ):
        if not isinstance( node, LifeNode ):
            raise "Given data is not an instance of class LifeNode"

    def __assertArrayOfNode( self, array ):
        if not isinstance( array, list ):
            raise "link() : Given param is not a list"
        for node in array:
            self.__assertIsNode( node )

    def link( self, linkArray ):
        self.__assertArrayOfNode( linkArray )
        if len(linkArray) > 8:
            raise "link() : Given node link array length is greater than 4"

        for i in range( 8 ):
            node = linkArray[i]
            if node is not None:
                self.__links[i] = node
        #self.__links = linkArray

    def isAlive( self ):
        return self.__alive

    def setAlive( self ):
        self.__alive = True

    def kill( self ):
        self.__alive = False

    #Private for now, to change in the future ?
    def __getNeighbourAlives( self ):
        alive = 0
        for node in self.__links:
            if node is not None:
                if node.isAlive():
                    alive += 1
        return alive

    def update( self ):
        neighbourAlive = self.__getNeighbourAlives()


    def linkNorth( self, node ):
        __assertIsNode( node )
        links[0] = node

    def linkNorthEast( self, node ):
        __assertIsNode( node )
        links[1] = node

    def linkEast( self, node ):
        __assertIsNode( node )
        links[2] = node

    def linkSouthEast( self, node ):
        __assertIsNode( node )
        links[3] = node

    def linkSouth( self, node ):
        __assertIsNode( node )
        links[4] = node

    def linkSouthWest( self, node ):
        __assertIsNode( node )
        links[5] = node

    def linkWest( self, node ):
        __assertIsNode( node )
        links[6] = node

    def linkNorthWest( self, node ):
        __assertIsNode( node )
        links[7] = node
