package ar.edu.itba.ss.integrators

import ar.edu.itba.ss.SimulationState
import kotlin.math.pow

class GearIntegrator(
    val dt: Double,
    private val initialR: DoubleArray,
    private val initialR1: DoubleArray,
    private val initialR2: DoubleArray,
    private val initialR3: DoubleArray,
    private val initialR4: DoubleArray,
    private val initialR5: DoubleArray,
    val accelerationUpdater: (Double, Int, DoubleArray, DoubleArray) -> Double
): Integrator {
    override fun iterator(): Iterator<SimulationState> {
        return object : Iterator<SimulationState> {
            private var time = 0.0

            private var r = initialR.clone()
            private var r1 = initialR1.clone()
            private var r2 = initialR2.clone()
            private var r3 = initialR3.clone()
            private var r4 = initialR4.clone()
            private var r5 = initialR5.clone()

            override fun hasNext(): Boolean {
                return true
            }

            override fun next(): SimulationState {
                val returnVal = SimulationState(time, r, r1)

                val r_p = DoubleArray(r.size)
                val r1_p = DoubleArray(r1.size)
                val r2_p = DoubleArray(r2.size)
                val r3_p = DoubleArray(r3.size)
                val r4_p = DoubleArray(r4.size)
                val r5_p = DoubleArray(r5.size)
                val delta = DoubleArray(r.size)

                for (i in r.indices) {
                    r_p[i] = r[i] + r1[i] * dt + r2[i] * dt.pow(2) / 2 + r3[i] * dt.pow(3) / 6 + r4[i] * dt.pow(4) / 24 + r5[i] * dt.pow(5) / 120
                    r1_p[i] = r1[i] + r2[i] * dt + r3[i] * dt.pow(2) / 2 + r4[i] * dt.pow(3)/6 + r5[i] * dt.pow(4)/24
                    r2_p[i] = r2[i] + r3[i] * dt + r4[i] * dt.pow(2) / 2 + r5[i] * dt.pow(3) / 6
                    r3_p[i] = r3[i] + r4[i] * dt + r5[i] * dt.pow(2) / 2
                    r4_p[i] = r4[i] + r5[i] * dt
                    r5_p[i] = r5[i]
                }

                val dt2 = dt * dt
                val dt3 = dt2 * dt
                val dt4 = dt3 * dt
                val dt5 = dt4 * dt

                for (i in r.indices) {
                    delta[i] = (accelerationUpdater(time + dt, i, r_p, r1_p) - r2_p[i]) * dt2 / 2
                    r[i] = r_p[i] + 3.0 / 16.0 * delta[i] // / dt ^ 0 = 1
                    r1[i] = r1_p[i] + 251.0 / 360.0 * delta[i] * 1.0 / dt
                    r2[i] = r2_p[i] + 1.0 * delta[i] * 2.0 / dt2
                    r3[i] = r3_p[i] + 11.0 / 18.0 * delta[i] * 6.0 / dt3
                    r4[i] = r4_p[i] + 1.0 / 6.0 * delta[i] * 24.0 / dt4
                    r5[i] = r5_p[i] + 1.0 / 60.0 * delta[i] * 120.0 / dt5
                }
                time += dt

                return returnVal
            }
        }
    }
}