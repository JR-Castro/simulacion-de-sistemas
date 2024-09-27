package ar.edu.itba.ss.integrators

import ar.edu.itba.ss.SimulationState

class VerletIntegrator(
    val dt: Double,
    private val positions: DoubleArray,
    private val speeds: DoubleArray,
    private val masses: DoubleArray,
    val forceUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double
) : Integrator {

    override fun iterator(): Iterator<SimulationState> {
        return object : Iterator<SimulationState> {
            private var time = 0.0

            private var currentR = positions
            private var previousR = positions.indices.map {
                positions[it] - speeds[it] * dt + 0.5 * forceUpdater(
                    time,
                    it,
                    positions,
                    speeds
                ) * dt * dt / masses[it]
            }.toDoubleArray()
            private var v = speeds

            override fun hasNext(): Boolean {
                return true
            }

            override fun next(): SimulationState {
                val returnVal = SimulationState(time, currentR, v)
                val newR = currentR.indices.map {
                    2 * currentR[it] - previousR[it] + forceUpdater(
                        time,
                        it,
                        currentR,
                        v
                    ) * dt * dt / masses[it]
                }.toDoubleArray()
                val newV = currentR.indices.map { (newR[it] - previousR[it]) / (2 * dt) }.toDoubleArray()

                time += dt
                previousR = currentR
                currentR = newR
                v = newV

                return returnVal
            }
        }
    }

}