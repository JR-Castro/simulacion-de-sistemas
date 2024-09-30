package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.GearIntegrator
import java.io.File
import kotlin.math.cos
import kotlin.math.pow

fun main() {
    val startTime = System.currentTimeMillis()

    val maxTime = 15.0
    val k = 100
    val amplitude = 10.0.pow(-2)
    val l0 = 10.0.pow(-3)
    val N = 1000
    val dt = 10.0.pow(-2)
    val w = 10.0.pow(1)

    val accelerationUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double = { time, i, r, v ->
        if (i == 0) {
            amplitude * cos(w * time) - k * (r[i] - r[i + 1])
        } else if (i == N - 1) {
            -k * (r[i] - r[i - 1])
        } else {
            -k * (r[i] - r[i - 1]) + k * (r[i + 1] - r[i])
        }
    }

    val initialR = DoubleArray(N) { 0.0 }
    val initialR1 = DoubleArray(N) { 0.0 }
    val initialR2 = initialR.indices.map { accelerationUpdater(0.0, it, initialR, initialR1) }.toDoubleArray()
    val initialR3 = DoubleArray(N) { 0.0 }
    val initialR4 = DoubleArray(N) { 0.0 }
    val initialR5 = DoubleArray(N) { 0.0 }

    val stateIterator = GearIntegrator(
        dt,
        initialR,
        initialR1,
        initialR2,
        initialR3,
        initialR4,
        initialR5,
        accelerationUpdater
    ).iterator()

    CSVWriter(File("coupled_oscillators.csv").bufferedWriter(bufferSize = 1024 * 1024 * 8)).use {
        do {
            val state = stateIterator.next()
            it.write(state)
        } while (state.time < maxTime)
    }

    println("Execution time: ${System.currentTimeMillis() - startTime}ms")

}