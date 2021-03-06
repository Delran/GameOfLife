

class LifeNode:

    # Links are clockwise starting at 0 o'clock
    #  links[0] = North
    #  links[1] = NorthEast
    #  links[2] = East
    #  links[3] = SouthEast
    #  links[4] = South
    #  links[5] = SouthWest
    #  links[6] = West
    #  links[7] = NorthWest
    __links = []
    __alive = False

    # True if will be alive at next generation
    # False otherwise
    __nextGen = True

    def __init__(self):
        #                N     NE    E     SE    S     SW    W     NW
        self.__links = [None, None, None, None, None, None, None, None]

    def __assertIsNode(self, node):
        if not isinstance(node, LifeNode):
            raise "Given data is not an instance of class LifeNode"

    def __assertArrayOfNode(self, array):
        if not isinstance(array, list):
            raise "link() : Given param is not a list"
        for node in array:
            self.__assertIsNode(node)

    def link(self, linkArray):
        self.__assertArrayOfNode(linkArray)
        if len(linkArray) > 8:
            raise "link() : Given node link array length is greater than 4"

        for i in range(8):
            node = linkArray[i]
            if node is not None:
                self.__links[i] = node
        # self.__links = linkArray

    def isAlive(self):
        return self.__alive

    def setAlive(self, alive):
        self.__alive = alive

    def kill(self):
        self.__alive = False

    # Private for now, to change in the future ?
    def __getNeighbourAlives(self):
        alive = 0
        for node in self.__links:
            if node is not None:
                if node.isAlive():
                    alive += 1
        return alive

    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    # Any live cell with two or three live neighbours lives on to the next generation.
    # Any live cell with more than three live neighbours dies, as if by overpopulation.
    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    def compute(self):
        neighbourAlive = self.__getNeighbourAlives()
        if self.__alive:
            if neighbourAlive < 2 or neighbourAlive > 3:
                self.__nextGen = False
        else:
            if neighbourAlive != 3:
                self.__nextGen = False

    def update(self):
        self.__alive = self.__nextGen
        self.__nextGen = True

    # Using an array to link nodes, keeping individual functions
    # just in case but are probably useless
    def linkNorth(self, node):
        self.__assertIsNode(node)
        self.links[0] = node

    def linkNorthEast(self, node):
        self.__assertIsNode(node)
        self.links[1] = node

    def linkEast(self, node):
        self.__assertIsNode(node)
        self.links[2] = node

    def linkSouthEast(self, node):
        self.__assertIsNode(node)
        self.links[3] = node

    def linkSouth(self, node):
        self.__assertIsNode(node)
        self.links[4] = node

    def linkSouthWest(self, node):
        self.__assertIsNode(node)
        self.links[5] = node

    def linkWest(self, node):
        self.__assertIsNode(node)
        self.links[6] = node

    def linkNorthWest(self, node):
        self.__assertIsNode(node)
        self.links[7] = node
