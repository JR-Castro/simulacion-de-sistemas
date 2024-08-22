package ar.edu.itba.ss

import ar.edu.itba.ss.files.DynamicInputCell

class Automaton2D(private val size: Int, initialCells: List<DynamicInputCell>, private val rules: Rules) :
    Iterator<Array<IntArray>> {
    private val previousStates = HashSet<Array<IntArray>>()
    private val cells = Array(size) { IntArray(size) }
    private var aliveCells = 0
    private var first = true

    init {
        initialCells.forEach {
            cells[it.x][it.y] = 1
        }
    }

    override fun next(): Array<IntArray> {
        previousStates.add(cells.map { it.clone() }.toTypedArray())
        val newCells = Array(size) { IntArray(size) }
        for (i in 0 until size) {
            for (j in 0 until size) {
                newCells[i][j] = rules.nextCellStatus2D(cells, i, j)
                aliveCells += newCells[i][j]
            }
        }

        cells.forEachIndexed { i, row ->
            row.forEachIndexed { j, _ ->
                cells[i][j] = newCells[i][j]
            }
        }

        return cells
    }

    override fun hasNext(): Boolean {
        if (aliveCells == 0 && !first)
            return false
        first = false
        if (cells[0].contains(1))
            return false
        if (cells[size - 1].contains(1))
            return false

        for (x in 1..size - 2) {
            if (cells[x][0] == 1)
                return false
            if (cells[x][size - 1] == 1)
                return false
        }

        return !previousStates.contains(cells)
    }


}