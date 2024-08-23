package ar.edu.itba.ss

import kotlin.math.abs

enum class Rules {
    CONWAY {
        override fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int {
            val aliveNeighbors = countAliveNeighborsMoore2D(cells, i, j, 1)
            return when {
                cells[i][j] == 1 && aliveNeighbors < 2 -> 0
                cells[i][j] == 1 && aliveNeighbors > 3 -> 0
                cells[i][j] == 0 && aliveNeighbors == 3 -> 1
                else -> cells[i][j]
            }
        }

        override fun nextCellStatus3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int): Int {
            val aliveNeighbors = countAliveNeighborsMoore3D(cells, i, j, k, 1)
            return when {
                cells[i][j][k] == 1 && aliveNeighbors < 2 -> 0
                cells[i][j][k] == 1 && aliveNeighbors > 3 -> 0
                cells[i][j][k] == 0 && aliveNeighbors == 3 -> 1
                else -> cells[i][j][k]
            }
        }
    },
    CONWAY_VON_NEUMANN {
        override fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int {
            val aliveNeighbors = countAliveNeighborsVonNeumann2D(cells, i, j, 1)
            return when {
                cells[i][j] == 1 && aliveNeighbors < 2 -> 0
                cells[i][j] == 1 && aliveNeighbors > 3 -> 0
                cells[i][j] == 0 && aliveNeighbors == 3 -> 1
                else -> cells[i][j]
            }
        }

        override fun nextCellStatus3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int): Int {
            val aliveNeighbors = countAliveNeighborsVonNeumann3D(cells, i, j, k, 1)
            return when {
                cells[i][j][k] == 1 && aliveNeighbors < 2 -> 0
                cells[i][j][k] == 1 && aliveNeighbors > 3 -> 0
                cells[i][j][k] == 0 && aliveNeighbors == 3 -> 1
                else -> cells[i][j][k]
            }
        }
    },
    DAVID_NEUMANN {
        override fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int {
            val aliveNeighbors = countAliveNeighborsVonNeumann2D(cells, i, j, 1)
            return when {
                cells[i][j] == 1 && aliveNeighbors == 4 -> 0
                cells[i][j] == 0 && aliveNeighbors == 1 -> 1
                else -> cells[i][j]
            }
        }

        override fun nextCellStatus3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int): Int {
            val aliveNeighbors = countAliveNeighborsVonNeumann3D(cells, i, j, k, 1)
            return when {
                cells[i][j][k] == 1 && aliveNeighbors == 6 -> 0
                cells[i][j][k] == 0 && aliveNeighbors == 1 -> 1
                else -> cells[i][j][k]
            }
        }
    };

    abstract fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int

    abstract fun nextCellStatus3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int): Int

    fun countAliveNeighborsMoore2D(cells: Array<IntArray>, i: Int, j: Int, r: Int): Int {
        var count = 0
        for (x in -r..r) {
            for (y in -r..r) {
                val neighbourX = i + x
                val neighbourY = j + y
                // We can do this because the board is a square
                if (neighbourX in cells.indices && neighbourY in cells.indices) {
                    count += cells[neighbourX][neighbourY]
                }
            }
        }
        count -= cells[i][j]
        return count
    }

    fun countAliveNeighborsVonNeumann2D(cells: Array<IntArray>, i: Int, j: Int, r: Int): Int {
        var count = 0
        for (x in -r..r) {
            for (y in (-r + abs(x))..(r - abs(x))) {
                val neighbourX = i + x
                val neighbourY = j + y
                // We can do this because the board is a square
                if (neighbourX in cells.indices && neighbourY in cells.indices) {
                    count += cells[neighbourX][neighbourY]
                }
            }
        }
        count -= cells[i][j]
        return count
    }

    fun countAliveNeighborsMoore3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int, r: Int): Int {
        var count = 0
        for (x in -r..r) {
            for (y in -r..r) {
                for (z in -r..r) {
                    val neighbourX = i + x
                    val neighbourY = j + y
                    val neighbourZ = k + z
                    // We can do this because the board is a cube
                    if (neighbourX in cells.indices && neighbourY in cells.indices && neighbourZ in cells.indices) {
                        count += cells[neighbourX][neighbourY][neighbourZ]
                    }
                }
            }
        }
        count -= cells[i][j][k]
        return count
    }

    fun countAliveNeighborsVonNeumann3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int, r: Int): Int {
        var count = 0
        for (x in -r..r) {
            for (y in (-r + abs(x))..(r - abs(x))) {
                for (z in (-r + abs(x) + abs(y))..(r - (abs(x) + abs(y)))) {
                    val neighbourX = i + x
                    val neighbourY = j + y
                    val neighbourZ = k + z
                    // We can do this because the board is a square
                    if (neighbourX in cells.indices && neighbourY in cells.indices && neighbourZ in cells.indices) {
                        count += cells[neighbourX][neighbourY][neighbourZ]
                    }
                }
            }
        }
        count -= cells[i][j][k]
        return count
    }
}