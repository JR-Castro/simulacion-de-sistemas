package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.BeemanIntegrator
import java.io.File
import kotlin.math.pow
import kotlin.math.sqrt

class GranularSimulation(
    n: Int,
    m: Int,
    val a0: Double,     // cm/s^2
    val T: Double,
    val dt: Double,
    val dt2: Double,
    val outputStates: File,
    val outputExits: File,
    val outputObstacles: File
) {
    // TODO: Change to use the units of the assignment instead of Kg, m, etc.
    companion object {
        private val W = 20              // cm
        private val L = 70              // cm
        private val particleRadius = 1.0// cm
        private val obstacleRadius = 1.0// cm

        // TODO: Get gamma from the previous TP, scaled to this k_n
        private val k_n = 250           // dina/m
        private val k_t = 2 * k_n       // dina/m
        private val gamma = 2.5         // g/m

        private val mass = 1.0          // g
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
    var particlesX = DoubleArray(n)
    var particlesY = DoubleArray(n)
    var speedsX = DoubleArray(n)
    var speedsY = DoubleArray(n)

    val collisions: MutableMap<Int, List<Int>> = HashMap()

    init {
        for (i in 0 until m) {
            var posX: Double
            var posY: Double
            do {
                posX = Math.random() * (L - 2 * obstacleRadius) + obstacleRadius
                posY = Math.random() * (W - 2 * obstacleRadius) + obstacleRadius
            } while ((0 until i).any {
                    (obstaclesX[it] - posX).pow(2) + (obstaclesY[it] - posY).pow(2) < (2.0 * obstacleRadius).pow(2)
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
                    (obstaclesX[it] - posX).pow(2) + (obstaclesY[it] - posY).pow(2) <
                            (obstacleRadius + particleRadius).pow(2)
                } || (0 until i).any {
                    (particlesX[it] - posX).pow(2) + (particlesY[it] - posY).pow(2) < (particleRadius * 2.0).pow(2)
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

        val integrator = BeemanIntegrator(
            dt,
            particlesX,
            speedsX,
            particlesY,
            speedsY,
            { time, i, x, x1, y, y1 ->
                if (collisions.isEmpty()) {
                    calculateCollisions(x, y)
                }

                var f_x = 0.0

                // Check collision with top wall
                if (y[i] + particleRadius >= W) {
                    val superposition = y[i] + particleRadius - W
                    val f_n = -k_n * superposition - gamma * speedsY[i]
                    val f_t = -k_t * superposition * x1[i]
                    f_x += f_n * TOP_WALL_NORM_X + f_t * TOP_WALL_TAN_X
                }
                if (y[i] - particleRadius <= 0) {
                    val superposition = y[i] - particleRadius
                    val f_n = -k_n * superposition - gamma * speedsY[i]
                    val f_t = -k_t * superposition * x1[i]
                    f_x += f_n * BOTTOM_WALL_NORM_X + f_t * BOTTOM_WALL_TAN_X
                }

                f_x / mass + a0
            },  // TODO: Calculate forces
            { time, i, x, x1, y, y1 ->
                if (collisions.isEmpty()) {
                    calculateCollisions(x, y)
                }

                var f_y = 0.0

                // Check collision with top wall
                if (y[i] + particleRadius >= W) {
                    val superposition = y[i] + particleRadius - W
                    val f_n = -k_n * superposition - gamma * speedsY[i]
                    val f_t = -k_t * superposition * x1[i]
                    f_y += f_n * TOP_WALL_NORM_Y + f_t * TOP_WALL_TAN_Y
                }
                if (y[i] - particleRadius <= 0) {
                    val superposition = y[i] - particleRadius
                    val f_n = -k_n * superposition - gamma * speedsY[i]
                    val f_t = -k_t * superposition * x1[i]
                    f_y += f_n * BOTTOM_WALL_NORM_Y + f_t * BOTTOM_WALL_TAN_Y
                }

                f_y / mass + a0
            },  // TODO: Calculate forces
            { time, i, x, x1, y, y1 -> x[i] }, // TODO: Detect when they crossed the limits
            { time, i, x, x1, y, y1 -> y[i] }
        ).iterator()

        var lastPrint = -dt2

        do {
            val state = integrator.next()
            // TODO: Detect when they crossed the limits
            particlesX = state.x
            particlesY = state.y
            speedsX = state.vx
            speedsY = state.vy
            collisions.clear()
            if (state.time - lastPrint >= dt2) {
                statesWriter.write(state)
                lastPrint = state.time
            }
        } while (state.time < T)
        statesWriter.close()
        exitsWriter.close()
    }

    fun calculateCollisions(x: DoubleArray, y: DoubleArray) {
        for (i in x.indices) {
            val collisionList = mutableListOf<Int>()
            for (j in x.indices) {
                if (i != j) {
                    val distance = sqrt((x[i] - x[j]).pow(2) + (y[i] - y[j]).pow(2))
                    if (distance < 2 * particleRadius) {
                        collisionList.add(j)
                    }
                }
            }
            for (j in obstaclesX.indices) {
                val distance = sqrt((x[i] - obstaclesX[j]).pow(2) + (y[i] - obstaclesY[j]).pow(2))
                if (distance < obstacleRadius + particleRadius) {
                    collisionList.add(j)
                }
            }
            collisions[i] = collisionList
        }
    }
}