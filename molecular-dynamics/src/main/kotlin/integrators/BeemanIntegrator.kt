package ar.edu.itba.ss.integrators

import ar.edu.itba.ss.SimulationState
import kotlin.math.pow

class BeemanIntegrator(
    val dt: Double,
    private val initialR: DoubleArray,
    private val initialR1: DoubleArray,
    val accelerationUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double
) : Integrator {

    override fun iterator(): Iterator<SimulationState> {
        return object : Iterator<SimulationState> {
            private var time = 0.0

            private var currentR = initialR
            private var currentV = initialR1

            private var previousR = initialR.indices.map {
                initialR[it] - initialR1[it] * dt + 0.5 * accelerationUpdater(
                    time, it, initialR, initialR1
                ) * dt.pow(2)
            }.toDoubleArray()
            private var previousV = initialR1.indices.map {
                initialR1[it] - accelerationUpdater(
                    time, it, initialR, initialR1
                ) * dt
            }.toDoubleArray()

            override fun hasNext(): Boolean {
                return true
            }

            override fun next(): SimulationState {
                val returnVal = SimulationState(time, currentR, currentV)

                val newR = currentR.indices.map {
                    currentR[it] +
                            currentV[it] * dt +
                            (2.0 / 3.0 * accelerationUpdater(time, it, currentR, currentV) -
                                    1.0 / 6.0 * accelerationUpdater(time - dt, it, previousR, previousV)) * dt.pow(2)
                }.toDoubleArray()

                val predictedV = currentV.indices.map {
                    currentV[it] +
                            3.0 / 2.0 * accelerationUpdater(time, it, currentR, currentV) * dt -
                            1.0 / 2.0 * accelerationUpdater(time - dt, it, previousR, previousV) * dt
                }.toDoubleArray()

                val newV = currentV.indices.map {
                    currentV[it] +
                            1.0 / 3.0 * accelerationUpdater(time + dt, it, newR, predictedV) * dt +
                            5.0 / 6.0 * accelerationUpdater(time, it, currentR, currentV) * dt -
                            1.0 / 6.0 * accelerationUpdater(time - dt, it, previousR, previousV) * dt
                }.toDoubleArray()

                time += dt
                previousR = currentR
                previousV = currentV
                currentR = newR
                currentV = newV

                return returnVal
            }
        }
    }
}