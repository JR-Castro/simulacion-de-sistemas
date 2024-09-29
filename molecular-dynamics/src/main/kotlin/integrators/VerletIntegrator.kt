package ar.edu.itba.ss.integrators

import ar.edu.itba.ss.SimulationState

class VerletIntegrator(
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
                    time,
                    it,
                    initialR,
                    initialR1
                ) * dt * dt
            }.toDoubleArray()

            override fun hasNext(): Boolean {
                return true
            }

            override fun next(): SimulationState {
                val returnVal = SimulationState(time, currentR, currentV)
                val newR = currentR.indices.map {
                    2 * currentR[it] - previousR[it] + accelerationUpdater(
                        time,
                        it,
                        currentR,
                        currentV
                    ) * dt * dt
                }.toDoubleArray()
                val newV = currentR.indices.map { (newR[it] - previousR[it]) / (2 * dt) }.toDoubleArray()

                time += dt
                previousR = currentR
                currentR = newR
                currentV = newV

                return returnVal
            }
        }
    }
}