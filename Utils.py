import numpy as np

import defs


def gridToMatrix(grid, height, length):
    matrix = np.zeros((height, length), dtype=float)

    for i in range(height):
        for j in range(length):
            matrix[i][j] = grid[i][j] is defs.ALIVECHAR

    return matrix

def matrixToLegacy(matrix):
    dim = np.shape(matrix)
    grid = []
    for i in range(dim[0]):
        row = []
        for j in range(dim[1]):
            char = defs.ALIVECHAR if matrix[i][j] else defs.DEADCHAR
            row.append(char)
        grid.append(row)

    return grid

def printGrid(grid):
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[0])):
            row.append(grid[i][j])
        print(row)

def printMatrix(matrix):
    for x in matrix:
        row = ""
        for y in x:
            if y:
                row += defs.ALIVECHAR
            else:
                row += defs.DEADCHAR
        print(row)
