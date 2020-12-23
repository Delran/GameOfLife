

class LifeNode:

    #Links are clockwise starting at 0 o'clock
    # links[0] = Up
    # links[1] = Right
    # links[2] = Down
    # links[3] = Left

    __links = []
    __alive = False

    def __init__( self ):
        #                Up    Right Down  Left
        self.__links = [ None, None, None, None ]

    def __assertIsNode( node ):
        if not isinstance( node, LifeNode ):
            raise "Given data is not an instance of class LifeNode"

    def __assertArrayOfNode( self, array ):
        if not isinstance( array, list ):
            raise "link() : Given param is not a list"
        for node in array:
            self.__assertIsNode( node )

    def link( self, linkArray ):
        self.__assertArrayOfNode( linkArray )
        if len(linkArray) > 4:
            raise "link() : Given node link array length is greater than 4"

        self.__links = linkArray

    

    def linkUp( self, node ):
        __assertIsNode( node )
        links[0] = node

    def linkRight( self, node ):
        __assertIsNode( node )
        links[1] = node

    def linkDown( self, node ):
        __assertIsNode( node )
        links[2] = node

    def linkLeft( self, node ):
        __assertIsNode( node )
        links[3] = node
