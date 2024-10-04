package ar.edu.itba.ss

import kotlinx.coroutines.*
import kotlinx.coroutines.selects.select
import java.io.File
import java.nio.file.Files

fun main(args: Array<String>) = runBlocking {
    val startTime = System.currentTimeMillis()

    val jobs = mutableListOf<Job>()

    for (a in args.withIndex()) {
        val file = a.value
        val fileName = file.split("/").last()
        val fileNameWithoutExtension = fileName.substring(0, fileName.length - 4)
        val outputFile = File("output/coupled_oscillator_$fileNameWithoutExtension.csv")
        val lines = Files.readAllLines(File(file).toPath())
        val maxtime = lines[0].toDouble()
        val k = lines[1].toDouble()
        val amplitude = lines[2].toDouble()
        val N = lines[3].toInt()
        val w = lines[4].toDouble()
        val dt = lines[5].toDouble()
        val dt2 = lines[6].toDouble()
        val mass = lines[7].toDouble()
        if (jobs.size == 12) {
            select<Unit> {
                jobs.forEach { job ->
                    job.onJoin {
                        jobs.remove(job) // Remove the completed job
                    }
                }
            }
        }
        jobs.add(launch(Dispatchers.IO) {
            CoupledOscillator(
                maxTime = maxtime,
                k = k,
                amplitude = amplitude,
                N = N,
                w = w,
                dt = dt,
                dt2 = dt2,
                mass = mass,
                outputFile
            ).run()
            println("Finished $file (${a.index}/${args.size})")
        })
    }

    jobs.joinAll()
    println("Execution time: ${System.currentTimeMillis() - startTime}ms")
}