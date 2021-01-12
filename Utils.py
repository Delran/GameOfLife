import numpy as np

import defs


def gridToMatrix(grid, height, length):
    matrix = np.zeros((height, length), dtype=float)

    for i in range(height):
        for j in range(length):
            matrix[i][j] = grid[i][j] is defs.ALIVECHAR

    return matrix


def printMatrix(matrix):
    for x in matrix:
        row = ""
        for y in x:
            if y:
                row += defs.ALIVECHAR
            else:
                row += defs.DEADCHAR
        print(row)
