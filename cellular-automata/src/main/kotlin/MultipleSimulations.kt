package ar.edu.itba.ss

import ar.edu.itba.ss.files.DynamicInput
import ar.edu.itba.ss.files.StaticInput
import com.github.ajalt.mordant.terminal.Terminal
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.nio.file.Files
import java.nio.file.Path
import kotlin.io.path.writeText

fun main(args: Array<String>) {
    if (args.size < 3) {
        println("Usage: <static_file> <dynamic_file> <output_file>")
        return
    }
    val staticFile = args[0]
    val dynamicFiles = args[1].split(",")
    val outputFiles = args[2].split(",")
    val terminal = Terminal()

    for (i in dynamicFiles.indices) {
        val staticInput = Json.decodeFromString<StaticInput>(Files.readString(Path.of(staticFile)))
        val dynamicInput = Json.decodeFromString<DynamicInput>(Files.readString(Path.of(dynamicFiles[i])))
        val outputFile = Path.of(outputFiles[i])

        val output =
            if (staticInput.is3D) run3DAutomata(staticInput, dynamicInput, terminal) else run2DAutomata(
                staticInput,
                dynamicInput,
                terminal
            )

        outputFile.writeText(Json.encodeToString(output))
    }
}