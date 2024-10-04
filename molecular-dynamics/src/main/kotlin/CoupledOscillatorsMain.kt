package ar.edu.itba.ss

import kotlinx.coroutines.Job
import kotlinx.coroutines.joinAll
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.io.File
import kotlin.math.min
import kotlin.math.pow

fun main() = runBlocking {
    val startTime = System.currentTimeMillis()

    val maxTime = 120.0
    val k = 100
    val amplitude = 10.0.pow(-2)
//    val l0 = 10.0.pow(-3)
    val N = 100
    val wValues = (0..8).map { 9.0 + it * 0.25 }
    val dtValues = wValues.map { min(1E-3, 1 / (100 * it)) }
    val dt2 = 0.05
    val mass = 0.001

    val jobs = mutableListOf<Job>()

    for (i in wValues.indices) {
        val outputFile = File("output/coupled_oscillator_w_$i.csv")
        jobs.add(launch {
            CoupledOscillator(
                maxTime,
                k.toDouble(),
                amplitude,
                N,
                wValues[i],
                dtValues[i],
                dt2,
                mass,
                outputFile
            ).run()
        })
    }

    jobs.joinAll()
    println("Execution time: ${System.currentTimeMillis() - startTime}ms")
}