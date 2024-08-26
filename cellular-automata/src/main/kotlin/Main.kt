package ar.edu.itba.ss

import ar.edu.itba.ss.files.DynamicInput
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

    override fun run() {
        val staticInput = Json.decodeFromString<StaticInput>(staticFile.readText())
        val dynamicInput = Json.decodeFromString<DynamicInput>(dynamicFile.readText())

        val output =
            if (staticInput.is3D) run3DAutomata(staticInput, dynamicInput, currentContext.terminal) else run2DAutomata(staticInput, dynamicInput, currentContext.terminal)

        outputFile.writeText(Json.encodeToString(output))
    }
}

fun main(args: Array<String>) = CellularAutomaton().main(args)