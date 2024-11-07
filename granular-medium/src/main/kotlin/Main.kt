package ar.edu.itba.ss

import java.io.File
import com.google.gson.Gson
import kotlinx.coroutines.*
import kotlinx.coroutines.selects.select

data class StaticInput(
    val a0: Double,
    val time: Double,
    val dt: Double,
    val dt2Interval: Int,
    val N: Int,
    val M: Int
)

data class DynamicInput(val particles: List<List<Double>>, val obstacles: List<List<Double>>)

fun outputFromInputFile(inputFile: String): Triple<String, String, String> {
    val fileName = inputFile.split("/").last()
    val parts = fileName.split(".")
    return Triple(
        "outputs/${parts[0]}_states.csv",
        "outputs/${parts[0]}_exits.csv",
        "outputs/${parts[0]}_obstacles.csv"
    )
}

fun main(args: Array<String>) = runBlocking {
    if (args.size < 2) {
        println("Usage: <static_input> [dynamic_input...]")
        return@runBlocking
    }

    val writeStates = args[0] != "--no-states"
    val start = if (writeStates) 0 else 1

    println("Running simulations")

    val startTime = System.currentTimeMillis()

    val jobs = mutableListOf<Job>()

    val maxConcurrentJobs = Runtime.getRuntime().availableProcessors()

    val gson = Gson()

    // Static input
    val staticData = gson.fromJson(File(args[start]).readText(), StaticInput::class.java)

    val dynamicFiles = args.slice(start + 1 until args.size)

    for (idxFile in dynamicFiles.withIndex()) {
        val idx = idxFile.index
        val file = idxFile.value

        if (jobs.size == maxConcurrentJobs) {
            select<Unit> {
                jobs.forEach { job ->
                    job.onJoin {
                        jobs.remove(job)
                    }
                }
            }
        }

        val filenames = outputFromInputFile(file)
        val dynamicData = gson.fromJson(File(file).readText(), DynamicInput::class.java)
        jobs.add(launch(Dispatchers.IO) {
            GranularSimulation(
                staticData.N,
                staticData.M,
                staticData.a0,
                staticData.time,
                staticData.dt,
                staticData.dt2Interval,
                dynamicData.obstacles,
                dynamicData.particles,
                if (writeStates) File(filenames.first) else null,
                File(filenames.second),
                File(filenames.third)
            ).run()
            println("Finished $file (${idx + 1}/${dynamicFiles.size})")
        })
    }

    jobs.joinAll()

    println("Execution time: ${System.currentTimeMillis() - startTime}ms")

}