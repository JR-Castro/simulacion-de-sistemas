package ar.edu.itba.ss

import ar.edu.itba.ss.files.DynamicInputCell
import com.github.ajalt.mordant.terminal.Terminal
import java.util.*

class Automaton2D(
    private val size: Int,
    initialCells: List<DynamicInputCell>,
    private val rules: Rules,
    private val terminal: Terminal
) :
    Iterator<Array<IntArray>> {
//    private val previousStates = LinkedList<Array<IntArray>>()
    private val cells = Array(size) { IntArray(size) }
    private var aliveCells = 0
    private var reachedEdge = false
    private var first = true

    init {
        initialCells.forEach {
            cells[it.x][it.y] = 1
        }
    }

    override fun next(): Array<IntArray> {
        aliveCells = 0
//        previousStates.add(cells.map { it.copyOf() }.toTypedArray())
        val newCells = Array(size) { IntArray(size) }
        for (i in 0 until size) {
            for (j in 0 until size) {
                newCells[i][j] = rules.nextCellStatus2D(cells, i, j)
                aliveCells += newCells[i][j]
                if ((i == 0 || i == size - 1 || j == 0 || j == size - 1) && newCells[i][j] == 1) {
                    reachedEdge = true
                }
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
        if (aliveCells == 0 && !first) {
            terminal.println(message = "All cells are dead", stderr = false)
            return false
        }
        first = false

        if (reachedEdge) {
            terminal.println(message = "Reached the edge", stderr = false)
            return false
        }

//        if (previousStates.any { prev -> prev contentDeepEquals cells }) {
//            terminal.println(message = "Reached a stable state", stderr = false)
//            return false
//        }

        return true
    }
}