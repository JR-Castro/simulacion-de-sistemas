package ar.edu.itba.ss.integrators

import ar.edu.itba.ss.SimulationState
import kotlin.math.pow

class BeemanIntegrator(
    val dt: Double,
    private val initialX: DoubleArray,
    private val initialVx: DoubleArray,
    private val initialY: DoubleArray,
    private val initialVy: DoubleArray,
    val accelerationCalculator: (Double, DoubleArray, DoubleArray, DoubleArray, DoubleArray) -> Pair<DoubleArray, DoubleArray>,
    val positionUpdater: (Double, DoubleArray, DoubleArray, DoubleArray, DoubleArray) -> Pair<DoubleArray, DoubleArray>,
) : Integrator {

    override fun iterator(): Iterator<SimulationState> {
        return object : Iterator<SimulationState> {
            private var time = 0.0

            private var currentX = initialX
            private var currentVx = initialVx
            private var currentY = initialY
            private var currentVy = initialVy


            private var previousX: DoubleArray
            private var previousY: DoubleArray
            private var previousVx: DoubleArray
            private var previousVy: DoubleArray

            init {
                val accelerations = accelerationCalculator(time, initialX, initialVx, initialY, initialVy)
                previousX = initialX.indices.map {
                    initialX[it] - initialVx[it] * dt + 0.5 * accelerations.first[it] * dt.pow(2)
                }.toDoubleArray()
                previousY = initialY.indices.map {
                    initialY[it] - initialVy[it] * dt + 0.5 * accelerations.second[it] * dt.pow(2)
                }.toDoubleArray()
                previousVx = initialVx.indices.map {
                    initialVx[it] - accelerations.first[it] * dt
                }.toDoubleArray()
                previousVy = initialVy.indices.map {
                    initialVy[it] - accelerations.second[it] * dt
                }.toDoubleArray()
            }

            override fun hasNext(): Boolean {
                return true
            }

            override fun next(): SimulationState {
                val returnVal =
                    SimulationState(time, currentX.clone(), currentVx.clone(), currentY.clone(), currentVy.clone())

                val accelerationsNow = accelerationCalculator(time, currentX, currentVx, currentY, currentVy)
                val accelerationsPast = accelerationCalculator(time - dt, previousX, previousVx, previousY, previousVy)

                val newX = currentX.indices.map {
                    currentX[it] + currentVx[it] * dt + (2.0 / 3.0 * accelerationsNow.first[it] - 1.0 / 6.0 * accelerationsPast.first[it]) * dt.pow(
                        2
                    )
                }.toDoubleArray()
                val newY = currentY.indices.map {
                    currentY[it] + currentVy[it] * dt + (2.0 / 3.0 * accelerationsNow.second[it] - 1.0 / 6.0 * accelerationsPast.second[it]) * dt.pow(
                        2
                    )
                }.toDoubleArray()

                val predictedVx = currentVx.indices.map {
                    currentVx[it] + 3.0 / 2.0 * accelerationsNow.first[it] * dt - 1.0 / 2.0 * accelerationsPast.first[it] * dt
                }.toDoubleArray()
                val predictedVy = currentVy.indices.map {
                    currentVy[it] + 3.0 / 2.0 * accelerationsNow.second[it] * dt - 1.0 / 2.0 * accelerationsPast.second[it] * dt
                }.toDoubleArray()

                val accelerationsNext = accelerationCalculator(time + dt, newX, predictedVx, newY, predictedVy)

                val newVx = currentVx.indices.map {
                    currentVx[it] + 1.0 / 3.0 * accelerationsNext.first[it] * dt + 5.0 / 6.0 * accelerationsNow.first[it] * dt - 1.0 / 6.0 * accelerationsPast.first[it] * dt
                }.toDoubleArray()
                val newVy = currentVy.indices.map {
                    currentVy[it] + 1.0 / 3.0 * accelerationsNext.second[it] * dt + 5.0 / 6.0 * accelerationsNow.second[it] * dt - 1.0 / 6.0 * accelerationsPast.second[it] * dt
                }.toDoubleArray()

                time += dt
                previousX = currentX
                previousY = currentY
                previousVx = currentVx
                previousVy = currentVy
                val updatedPositions = positionUpdater(time, newX, newVx, newY, newVy)
                currentX = updatedPositions.first
                currentY = updatedPositions.second
                currentVx = newVx
                currentVy = newVy

                return returnVal
            }
        }
    }
}