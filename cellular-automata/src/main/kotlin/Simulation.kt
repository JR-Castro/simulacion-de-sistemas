package ar.edu.itba.ss

import ar.edu.itba.ss.files.DynamicInput
import ar.edu.itba.ss.files.DynamicInputCell
import ar.edu.itba.ss.files.DynamicInputState
import ar.edu.itba.ss.files.StaticInput
import com.github.ajalt.mordant.terminal.Terminal

fun run2DAutomata(staticInput: StaticInput, dynamicInput: DynamicInput, terminal: Terminal): List<DynamicInputState> {
    val automaton = Automaton2D(
        staticInput.areaSize,
        dynamicInput.moments.first().cells,
        staticInput.rules,
        terminal
    )

    var i = 0
    val output = mutableListOf<DynamicInputState>()
    output.add(i, dynamicInput.moments.first())
    while (automaton.hasNext() && i < staticInput.maxIterations) {
        i++
        val cells = automaton.next()
        val newCells = cells.mapIndexed { x, xrow ->
            xrow.mapIndexed { y, cell ->
                if (cell != 0) {
                    DynamicInputCell(
                        x,
                        y,
                        state = cell
                    )
                } else {
                    null
                }
            }.filterNotNull()
        }.flatten()

        output.add(
            DynamicInputState(
                i,
                newCells
            )
        )
    }

    if (i == staticInput.maxIterations) {
        terminal.println(message = "Reached max iterations", stderr = false)
    }

    return output
}

fun run3DAutomata(staticInput: StaticInput, dynamicInput: DynamicInput, terminal: Terminal): List<DynamicInputState> {
    val automaton = Automaton3D(
        staticInput.areaSize,
        dynamicInput.moments.first().cells,
        staticInput.rules,
        terminal
    )

    var i = 0
    val output = mutableListOf<DynamicInputState>()
    output.add(i, dynamicInput.moments.first())
    while (automaton.hasNext() && i < staticInput.maxIterations) {
        i++
        val cells = automaton.next()
        val newCells = cells.mapIndexed { x, xrow ->
            xrow.mapIndexed { y, yrow ->
                yrow.mapIndexed { z, cell ->
                    if (cell != 0) {
                        DynamicInputCell(
                            x,
                            y,
                            z,
                            cell
                        )
                    } else {
                        null
                    }
                }.filterNotNull()
            }.flatten()
        }.flatten()

        output.add(
            DynamicInputState(
                i, newCells
            )
        )

    }

    if (i == staticInput.maxIterations) {
        terminal.println(message = "Reached max iterations", stderr = false)
    }

    return output
}
