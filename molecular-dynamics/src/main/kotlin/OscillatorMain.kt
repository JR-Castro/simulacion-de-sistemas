package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.GearIntegrator
import java.io.BufferedWriter
import java.io.FileWriter
import kotlin.math.pow


fun main() {
    val startTime = System.currentTimeMillis()

    val maxTime = 5.0
    val k = 10.0.pow(4)
    val mass = 70.0
    val gamma = 100.0
    val startPos = 1.0
    val startSpeed = -1 * 100 / (2 * mass)
    val stepsToWrite = 1000

    val accelerationUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double = { time, i, r, v ->
        (-k * r[i] - gamma * v[i]) / mass
    }

    val initialR = doubleArrayOf(startPos)
    val initialR1 = doubleArrayOf(startSpeed)
    val initialR2 = doubleArrayOf(-k / mass * startPos)
    val initialR3 = doubleArrayOf(-k / mass * initialR1[0])
    val initialR4 = doubleArrayOf(-k / mass * initialR2[0])
    val initialR5 = doubleArrayOf(-k / mass * initialR3[0])

    val writer = BufferedWriter(FileWriter("outputGear.txt"), 1024 * 1024 * 8)
    val csvWriter = CSVFormatter(writer)

    val integrator =
        GearIntegrator(1e-5, initialR, initialR1, initialR2, initialR3, initialR4, initialR5, accelerationUpdater).iterator()

    var currentStep = 0
    var lastWritten = -stepsToWrite

    do {
        val state = integrator.next()
        if (currentStep - lastWritten >= stepsToWrite) {
            csvWriter.write(state)
            lastWritten = currentStep
        }
        currentStep++
    } while (state.time < maxTime)

    writer.close()

    println("Execution time: ${System.currentTimeMillis() - startTime} ms")
}