package ar.edu.itba.ss.integrators

import ar.edu.itba.ss.SimulationState
import kotlin.math.pow

class BeemanIntegrator(
    val dt: Double,
    private val initialX: DoubleArray,
    private val initialVx: DoubleArray,
    private val initialY: DoubleArray,
    private val initialVy: DoubleArray,
    val accelerationUpdaterX: (Double, Int, DoubleArray, DoubleArray, DoubleArray, DoubleArray) -> Double,
    val accelerationUpdaterY: (Double, Int, DoubleArray, DoubleArray, DoubleArray, DoubleArray) -> Double,
    val positionUpdaterX: (Double, Int, DoubleArray, DoubleArray, DoubleArray, DoubleArray) -> Double,
    val positionUpdaterY: (Double, Int, DoubleArray, DoubleArray, DoubleArray, DoubleArray) -> Double
) : Integrator {

    override fun iterator(): Iterator<SimulationState> {
        return object : Iterator<SimulationState> {
            private var time = 0.0

            private var currentX = initialX
            private var currentVx = initialVx
            private var currentY = initialY
            private var currentVy = initialVy

            private var previousX = initialX.indices.map {
                initialX[it] - initialVx[it] * dt + 0.5 * accelerationUpdaterX(
                    time, it, initialX, initialVx, initialY, initialVy
                ) * dt.pow(2)
            }.toDoubleArray()
            private var previousY = initialY.indices.map {
                initialY[it] - initialVy[it] * dt + 0.5 * accelerationUpdaterY(
                    time, it, initialX, initialVx, initialY, initialVy
                ) * dt.pow(2)
            }.toDoubleArray()
            private var previousVx = initialVx.indices.map {
                initialVx[it] - accelerationUpdaterX(
                    time, it, initialX, initialVx, initialY, initialVy
                ) * dt
            }.toDoubleArray()
            private var previousVy = initialVy.indices.map {
                initialVy[it] - accelerationUpdaterY(
                    time, it, initialX, initialVx, initialY, initialVy
                ) * dt
            }.toDoubleArray()

            override fun hasNext(): Boolean {
                return true
            }

            override fun next(): SimulationState {
                val returnVal = SimulationState(time, currentX.clone(), currentVx.clone(), currentY.clone(), currentVy.clone())

                val newX = currentX.indices.map {
                    currentX[it] +
                            currentVx[it] * dt +
                            (2.0 / 3.0 * accelerationUpdaterX(time, it, currentX, currentVx, currentY, currentVy) -
                                    1.0 / 6.0 * accelerationUpdaterX(time - dt, it, previousX, previousVx, currentY, currentVy)) * dt.pow(2)
                }.toDoubleArray()
                val newY = currentY.indices.map {
                    currentY[it] +
                            currentVy[it] * dt +
                            (2.0 / 3.0 * accelerationUpdaterY(time, it, currentX, currentVx, currentY, currentVy) -
                                    1.0 / 6.0 * accelerationUpdaterY(time - dt, it, previousX, previousVx, currentY, currentVy)) * dt.pow(2)
                }.toDoubleArray()

                val predictedVx = currentVx.indices.map {
                    currentVx[it] +
                            3.0 / 2.0 * accelerationUpdaterX(time, it, currentX, currentVx, currentY, currentVy) * dt -
                            1.0 / 2.0 * accelerationUpdaterX(time - dt, it, previousX, previousVx, previousY, previousVy) * dt
                }.toDoubleArray()
                val predictedVy = currentVy.indices.map {
                    currentVy[it] +
                            3.0 / 2.0 * accelerationUpdaterY(time, it, currentX, currentVx, currentY, currentVy) * dt -
                            1.0 / 2.0 * accelerationUpdaterY(time - dt, it, previousX, previousVx, previousY, previousVy) * dt
                }.toDoubleArray()

                val newVx = currentVx.indices.map {
                    currentVx[it] +
                            1.0 / 3.0 * accelerationUpdaterX(time + dt, it, newX, predictedVx, newY, predictedVy) * dt +
                            5.0 / 6.0 * accelerationUpdaterX(time, it, currentX, currentVx, currentY, currentVy) * dt -
                            1.0 / 6.0 * accelerationUpdaterX(time - dt, it, previousX, previousVx, previousY, previousVy) * dt
                }.toDoubleArray()
                val newVy = currentVy.indices.map {
                    currentVy[it] +
                            1.0 / 3.0 * accelerationUpdaterY(time + dt, it, newX, predictedVx, newY, predictedVy) * dt +
                            5.0 / 6.0 * accelerationUpdaterY(time, it, currentX, currentVx, currentY, currentVy) * dt -
                            1.0 / 6.0 * accelerationUpdaterY(time - dt, it, previousX, previousVx, previousY, previousVy) * dt
                }.toDoubleArray()

                time += dt
                previousX = currentX
                previousY = currentY
                previousVx = currentVx
                previousVy = currentVy
                currentX = newX.indices.map { positionUpdaterX(time, it, newX, newVx, newY, newVy) }.toDoubleArray()
                currentY = newX.indices.map { positionUpdaterY(time, it, newX, newVx, newY, newVy) }.toDoubleArray()
                currentVx = newVx
                currentVy = newVy

                return returnVal
            }
        }
    }
}