package ar.edu.itba.ss

import ar.edu.itba.ss.files.DynamicInputCell

class Automaton3D(private val size: Int, initialCells: List<DynamicInputCell>, private val rules: Rules) :
    Iterator<Array<Array<IntArray>>> {
    private val previousStates = HashSet<Array<Array<IntArray>>>()
    private val cells = Array(size) { Array(size) { IntArray(size) } }
    private var aliveCells = 0
    private var reachedEdge = false
    private var first = true

    init {
        initialCells.forEach {
            cells[it.x][it.y][it.z] = 1
        }
    }

    override fun next(): Array<Array<IntArray>> {
        aliveCells = 0
        previousStates.add(cells.map { xrow -> xrow.map { yrow -> yrow.clone() }.toTypedArray() }.toTypedArray())
        val newCells = Array(size) { Array(size) { IntArray(size) } }
        for (i in 0 until size) {
            for (j in 0 until size) {
                for (k in 0 until size) {
                    newCells[i][j][k] = rules.nextCellStatus3D(cells, i, j, k)
                    aliveCells += newCells[i][j][k]
                    if ((i == 0 || i == size -1 || j == 0 || j == size - 1 || k == 0 || k == size - 1) && newCells[i][j][k] == 1) {
                        reachedEdge = true
                    }
                }
            }
        }

        cells.forEachIndexed { i, row ->
            row.forEachIndexed { j, _ ->
                row.forEachIndexed { k, _ ->
                    cells[i][j][k] = newCells[i][j][k]
                }
            }
        }

        return cells
    }

    override fun hasNext(): Boolean {
        if (aliveCells == 0 && !first)
            return false
        first = false

        if (reachedEdge)
            return false

        return !previousStates.contains(cells)
    }
}