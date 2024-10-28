package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.BeemanIntegrator
import java.io.File
import kotlin.math.pow
import kotlin.math.sqrt

class GranularSimulation(
    n: Int,
    m: Int,
    val a0: Double,
    val T: Double,
    val dt: Double,
    val dt2: Double,
    val outputStates: File,
    val outputExits: File,
    val outputObstacles: File
) {
    companion object {
        private val W = 0.2         // cm
        private val L = 0.7         // cm
        private val particleRadius = 0.01        // cm
        private val obstacleRadius = 0.01        // cm
        private val k_n = 0.25      // N/m
        private val k_t = 2 * k_n   // N/m
        private val mass = 0.001       // Kg
        private val obstacleMass: Double = Double.POSITIVE_INFINITY

        private val TOP_WALL_NORM_X = 0.0
        private val TOP_WALL_NORM_Y = 1.0
        private val TOP_WALL_TAN_X = -TOP_WALL_NORM_Y
        private val TOP_WALL_TAN_Y = TOP_WALL_NORM_X

        private val BOTTOM_WALL_NORM_X = 0.0
        private val BOTTOM_WALL_NORM_Y = -1.0
        private val BOTTOM_WALL_TAN_X = -BOTTOM_WALL_NORM_Y
        private val BOTTOM_WALL_TAN_Y = BOTTOM_WALL_NORM_X
    }

    val obstaclesX = DoubleArray(m)
    val obstaclesY = DoubleArray(m)
    val particlesX = DoubleArray(n)
    val particlesY = DoubleArray(n)
    val speedsX = DoubleArray(n)
    val speedsY = DoubleArray(n)

    init {
        for (i in 0 until m) {
            var posX: Double
            var posY: Double
            do {
                posX = Math.random() * (L - 2 * obstacleRadius) + obstacleRadius
                posY = Math.random() * (W - 2 * obstacleRadius) + obstacleRadius
            } while ((0 until i).any {
                    sqrt((obstaclesX[i] - posX).pow(2) + (obstaclesY[i] - posY).pow(2)) < 2 * obstacleRadius
                })
            obstaclesX[i] = posX
            obstaclesY[i] = posY
        }
        for (i in 0 until n) {
            var posX: Double
            var posY: Double
            do {
                posX = Math.random() * (L - 2 * particleRadius) + particleRadius
                posY = Math.random() * W
            } while (
                (0 until m).any {
                    sqrt((obstaclesX[i] - posX).pow(2) + (obstaclesY[i] - posY).pow(2)) < obstacleRadius + particleRadius
                } || (0 until i).any {
                    sqrt((particlesX[i] - posX).pow(2) + (particlesY[i] - posY).pow(2)) < particleRadius * 2
                }
            )
            particlesX[i] = posX
            particlesY[i] = posY
            speedsX[i] = 0.0
            speedsY[i] = 0.0
        }
    }

    fun run() {
        CSVWriter(outputObstacles.writer()).use {
            it.writeObstacles(obstaclesX, obstaclesY)
        }

        val statesWriter = CSVWriter(outputStates.bufferedWriter(bufferSize = 1024 * 1024 * 8))
        val exitsWriter = CSVWriter(outputExits.bufferedWriter(bufferSize = 1024 * 1024 * 8))

        val xIntegrator = BeemanIntegrator(
            dt,
            particlesX,
            speedsX,
            { time, i, r, r1 -> a0 },  // TODO: Calculate forces
            { time, i, r, r1 -> r[i] } // TODO: Detect when they crossed the limits
        ).iterator()
        val yIntegrator = BeemanIntegrator(
            dt,
            particlesY,
            speedsY,
            { time, i, r, r1 -> 0.0 },  // TODO: Calculate forces
            { time, i, r, r1 -> r[i] }
        ).iterator()

        var lastPrint = -dt2

        do {
            val xState = xIntegrator.next()
            val yState = yIntegrator.next()
            // TODO: Detect when they crossed the limits
            if (xState.time != yState.time) throw IllegalStateException("Different Times")
            if (xState.time - lastPrint >= dt2) {
                statesWriter.write(xState, yState)
                lastPrint = xState.time
            }
        } while (xState.time < T && yState.time < T)
        statesWriter.close()
        exitsWriter.close()
    }
}