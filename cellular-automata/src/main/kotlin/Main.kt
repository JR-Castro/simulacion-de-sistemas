package ar.edu.itba.ss

import ar.edu.itba.ss.files.DynamicInput
import ar.edu.itba.ss.files.DynamicInputCell
import ar.edu.itba.ss.files.DynamicInputState
import ar.edu.itba.ss.files.StaticInput
import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.arguments.argument
import com.github.ajalt.clikt.parameters.arguments.validate
import com.github.ajalt.clikt.parameters.types.file
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

class CellularAutomaton : CliktCommand() {
    private val staticFile by argument("static", help = "Static file path")
        .file(mustExist = true, canBeDir = false)
        .validate { require(it.exists()) { "Static file must exist" } }
    private val dynamicFile by argument("dynamic", help = "Dynamic file path")
        .file(mustExist = true, canBeDir = false)
        .validate { require(it.exists()) { "Dynamic file must exist" } }
    private val outputFile by argument("output", help = "Output file path").file(canBeDir = false)

    private fun run2DAutomata(staticInput: StaticInput, dynamicInput: DynamicInput): List<DynamicInputState> {
        val automaton = Automaton2D(
            staticInput.areaSize,
            dynamicInput.moments.first().cells,
            staticInput.rules,
            currentContext.terminal
        )

        var i = 0
        val output = mutableListOf<DynamicInputState>()
        output.add(i, dynamicInput.moments.first())
        while (automaton.hasNext()) {
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

        return output
    }

    private fun run3DAutomata(staticInput: StaticInput, dynamicInput: DynamicInput): List<DynamicInputState> {
        val automaton = Automaton3D(
            staticInput.areaSize,
            dynamicInput.moments.first().cells,
            staticInput.rules,
            currentContext.terminal
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
            currentContext.terminal.println(message = "Reached max iterations", stderr = false)
        }

        return output
    }

    override fun run() {
        val staticInput = Json.decodeFromString<StaticInput>(staticFile.readText())
        val dynamicInput = Json.decodeFromString<DynamicInput>(dynamicFile.readText())

        val output =
            if (staticInput.is3D) run3DAutomata(staticInput, dynamicInput) else run2DAutomata(staticInput, dynamicInput)

        outputFile.writeText(Json.encodeToString(output))
    }
}

fun main(args: Array<String>) = CellularAutomaton().main(args)