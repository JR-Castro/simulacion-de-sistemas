package ar.edu.itba.ss.integrators

import ar.edu.itba.ss.SimulationState

class VerletIntegrator(
    val dt: Double,
    private val initialR: DoubleArray,
    private val initialR1: DoubleArray,
    val accelerationUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double,
    val positionUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double
) : Integrator {

    override fun iterator(): Iterator<SimulationState> {
        return object : Iterator<SimulationState> {
            private var time = 0.0

            // r(t)
            private var currentR = initialR

            // v(t)
            private var currentV = initialR1

            private var previousR = initialR.indices.map {
                initialR[it] - initialR1[it] * dt + 0.5 * accelerationUpdater(
                    time,
                    it,
                    initialR,
                    initialR1
                ) * dt * dt
            }.toDoubleArray()

            // r(t+dt)
            private var nextR = initialR.indices.map {
                2.0 * currentR[it] - previousR[it] + dt * dt * accelerationUpdater(time, it, initialR, initialR1)
            }.toDoubleArray()


            override fun hasNext(): Boolean = true

            override fun next(): SimulationState {
                val returnVal = SimulationState(time, currentR.clone(), currentV.clone())

                time += dt

                previousR = currentR
                currentR = nextR

                val newNextR = currentR.indices.map {
                    2.0 * currentR[it] - previousR[it] + dt * dt * accelerationUpdater(time, it, currentR, currentV)
                }.toDoubleArray()
                nextR = newNextR.indices.map { positionUpdater(time, it, newNextR, currentV) }.toDoubleArray()

                currentV = nextR.indices.map {
                    (nextR[it] - previousR[it]) / (2.0 * dt)
                }.toDoubleArray()

                return returnVal
            }
        }
    }
}