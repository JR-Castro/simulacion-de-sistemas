package ar.edu.itba.ss

enum class Rules {
    CONWAY {
        override fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int {
            val aliveNeighbours = countAliveNeighbours2D(cells, i, j)
            return when {
                cells[i][j] == 1 && aliveNeighbours < 2 -> 0
                cells[i][j] == 1 && aliveNeighbours > 3 -> 0
                cells[i][j] == 0 && aliveNeighbours == 3 -> 1
                else -> cells[i][j]
            }
        }
    };

    abstract fun nextCellStatus2D(cells: Array<IntArray>, i: Int, j: Int): Int

    fun countAliveNeighbours2D(cells: Array<IntArray>, i: Int, j: Int): Int {
        var count = 0
        for (x in -1..1) {
            for (y in -1..1) {
                val neighbourX = i + x
                val neighbourY = j + y
                if (neighbourX in cells.indices && neighbourY in cells.indices) {
                    count += cells[neighbourX][neighbourY]
                }
            }
        }
        count -= cells[i][j]
        return count
    }
}