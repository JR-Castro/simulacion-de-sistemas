package ar.edu.itba.ss

import kotlinx.coroutines.Job
import kotlinx.coroutines.joinAll
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.io.File
import java.nio.file.Files

fun main(args: Array<String>) = runBlocking {
    val startTime = System.currentTimeMillis()

    val files = args.sliceArray(0 until args.size)

    val jobs = mutableListOf<Job>()

    for (file in files) {
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
        jobs.add(launch {
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
        })
    }

    jobs.joinAll()
    println("Execution time: ${System.currentTimeMillis() - startTime}ms")
}