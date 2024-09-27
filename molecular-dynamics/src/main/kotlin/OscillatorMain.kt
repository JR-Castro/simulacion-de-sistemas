package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.BeemanIntegrator
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
//    val startAcceleration = -10e4 * startPos - 100 * startSpeed

    val writer = BufferedWriter(FileWriter("outputBeeman.txt"), 1024 * 1024 * 8)
    val csvWriter = CSVFormatter(writer)

    val integrator = BeemanIntegrator(
        1e-4,
        doubleArrayOf(startPos),
        doubleArrayOf(startSpeed),
    ) { time, i, r, v ->
        (-k * r[i] - gamma * v[i]) / mass
    }.iterator()

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