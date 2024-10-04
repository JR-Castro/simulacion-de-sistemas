package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.VerletIntegrator
import java.io.File
import kotlin.math.sin

class CoupledOscillator(
    val maxTime: Double,
    val k: Double,
    val amplitude: Double,
    val N: Int,
    val w: Double,
    val dt: Double,
    val dt2: Double,
    val mass: Double,
    val outputFile: File
) {
    private val accelerationUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double = { _, i, r, _ ->
        if (i == 0 || i == N - 1) {
            0.0
        } else {
            (-k * (r[i] - r[i - 1]) + k * (r[i + 1] - r[i])) / mass
        }
    }

    private val positionUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double = { t, i, r, r1 ->
        if (i == 0) {
            amplitude * sin(w * t)
        } else {
            r[i]
        }
    }

    val initialR = DoubleArray(N) { 0.0 }
    val initialR1 = DoubleArray(N) { 0.0 }
    val initialR2 = initialR.indices.map { accelerationUpdater(0.0, it, initialR, initialR1) }.toDoubleArray()
    val initialR3 = DoubleArray(N) { 0.0 }
    val initialR4 = DoubleArray(N) { 0.0 }
    val initialR5 = DoubleArray(N) { 0.0 }

    val stateIterator = VerletIntegrator(
        dt,
        initialR,
        initialR1,
        accelerationUpdater,
        positionUpdater
    ).iterator()

    fun run() {
        var lastWritten = -dt2
        CSVWriter(outputFile.bufferedWriter(bufferSize = 1024 * 1024 * 8)).use {
            do {
                val state = stateIterator.next()
                if (state.time - lastWritten >= dt2) {
                    it.write(state)
                    lastWritten = state.time
                }
            } while (state.time < maxTime)
        }
    }
}