package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.BeemanIntegrator
import ar.edu.itba.ss.integrators.GearIntegrator
import ar.edu.itba.ss.integrators.VerletIntegrator
import java.io.File
import kotlin.math.pow

fun testIntegrator(states: Iterator<SimulationState>, output: String, dt2: Double, maxTime: Double) {
    var lastWritten = -dt2

    CSVWriter(File(output).bufferedWriter(bufferSize = 1024 * 1024 * 8)).use {
        do {
            val state = states.next()
            if (state.time - lastWritten >= dt2) {
                it.write(state)
                lastWritten = state.time
            }
        } while (state.time < maxTime)
    }
}

fun main() {
    val startTime = System.currentTimeMillis()

    val maxTime = 5.0
    val k = 10.0.pow(4)
    val mass = 70.0
    val gamma = 100.0
    val startPos = 1.0
    val startSpeed = -1 * 100 / (2 * mass)

    val accelerationUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double = { time, i, r, v ->
        (-k * r[i] - gamma * v[i]) / mass
    }

    val initialR = doubleArrayOf(startPos)
    val initialR1 = doubleArrayOf(startSpeed)
    val initialR2 = doubleArrayOf(-k / mass * startPos)
    val initialR3 = doubleArrayOf(-k / mass * initialR1[0])
    val initialR4 = doubleArrayOf(-k / mass * initialR2[0])
    val initialR5 = doubleArrayOf(-k / mass * initialR3[0])

    for (i in 1 until 8) {
        val dt = 0.1.pow(i)
        val dt2 = 0.005
        println("dt: $dt")
        val verletIterator = VerletIntegrator(
            dt,
            initialR,
            initialR1,
            accelerationUpdater
        ).iterator()
        val beemanIterator = BeemanIntegrator(
            dt,
            initialR,
            initialR1,
            accelerationUpdater
        ).iterator()
        val gearIterator = GearIntegrator(
            dt,
            initialR,
            initialR1,
            initialR2,
            initialR3,
            initialR4,
            initialR5,
            accelerationUpdater
        ).iterator()

        testIntegrator(verletIterator, "outputVerlet_${i}.txt", dt2, maxTime)
        testIntegrator(beemanIterator, "outputBeeman_${i}.txt", dt2, maxTime)
        testIntegrator(gearIterator, "outputGear_${i}.txt", dt2, maxTime)
    }



    println("Execution time: ${System.currentTimeMillis() - startTime} ms")
}