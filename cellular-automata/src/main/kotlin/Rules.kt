package ar.edu.itba.ss

enum class Rules {
    CONWAY {
        override fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int {
            val aliveNeighbors = countAliveNeighbors2D(cells, i, j)
            return when {
                cells[i][j] == 1 && aliveNeighbors < 2 -> 0
                cells[i][j] == 1 && aliveNeighbors > 3 -> 0
                cells[i][j] == 0 && aliveNeighbors == 3 -> 1
                else -> cells[i][j]
            }
        }

        override fun nextCellStatus3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int): Int {
            val aliveNeighbors = countAliveNeighbors3D(cells, i, j, k)
            return when {
                cells[i][j][k] == 1 && aliveNeighbors < 2 -> 0
                cells[i][j][k] == 1 && aliveNeighbors > 3 -> 0
                cells[i][j][k] == 0 && aliveNeighbors == 3 -> 1
                else -> cells[i][j][k]
            }
        }
    };

    abstract fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int

    abstract fun nextCellStatus3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int): Int

    fun countAliveNeighbors2D(cells: Array<IntArray>, i: Int, j: Int): Int {
        var count = 0
        for (x in -1..1) {
            for (y in -1..1) {
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

    fun countAliveNeighbors3D(cells: Array<Array<IntArray>>, i: Int, j: Int, k: Int): Int {
        var count = 0
        for (x in -1..1) {
            for (y in -1..1) {
                for (z in -1..1) {
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
}