package ar.edu.itba.ss

import ar.edu.itba.ss.integrators.BeemanIntegrator
import java.io.File
import kotlin.math.pow
import kotlin.math.round
import kotlin.math.sqrt

class GranularSimulation(
    n: Int,
    m: Int,
    val a0: Double,     // cm/s^2
    val T: Double,
    val dt2Interval: Int,
    val outputStates: File,
    val outputExits: File,
    val outputObstacles: File
) {
    companion object {
        private val W = 20              // cm
        private val L = 70              // cm
        private val particleRadius = 1.0// cm
        private val obstacleRadius = 1.0// cm

        private val k_n = 250           // dina/m
        private val k_t = 2 * k_n       // dina/m
        private val gamma = 2.5         // g/m

        private val mass = 1.0          // g

//        private val dt = 0.1 * sqrt(mass / k_n) // s
        private val dt = 1E-3

        private val TOP_WALL_NORM_X = 0.0
        private val TOP_WALL_NORM_Y = 1.0
        private val TOP_WALL_TAN_X = -TOP_WALL_NORM_Y
        private val TOP_WALL_TAN_Y = TOP_WALL_NORM_X

        private val BOTTOM_WALL_NORM_X = 0.0
        private val BOTTOM_WALL_NORM_Y = -1.0
        private val BOTTOM_WALL_TAN_X = -BOTTOM_WALL_NORM_Y
        private val BOTTOM_WALL_TAN_Y = BOTTOM_WALL_NORM_X
    }

    private val obstaclesX = DoubleArray(m)
    private val obstaclesY = DoubleArray(m)
    private var particlesX = DoubleArray(n)
    private var particlesY = DoubleArray(n)
    private var speedsX = DoubleArray(n)
    private var speedsY = DoubleArray(n)

    private val obstacleCollisions: MutableMap<Int, List<Int>> = HashMap()
    private val particleCollisions: MutableMap<Int, List<Int>> = HashMap()
    private val particleCrossings: MutableMap<Double, MutableList<ParticleExit>> = HashMap()

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
                posX = Math.random() * L
                posY = Math.random() * (W - 2 * particleRadius) + particleRadius
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
            { _, i, x, x1, y, y1 -> calculateForces(i, x, x1, y, y1).first },
            { _, i, x, x1, y, y1 -> calculateForces(i, x, x1, y, y1).second },
            { time, i, x, x1, y, y1 ->
                when {
                    x[i] >= L -> {
                        val list = particleCrossings.getOrDefault(time, mutableListOf())
                        list.add(ParticleExit(time, x[i], y[i], x1[i], y1[i]))
                        particleCrossings[time] = list
                        x[i] % L
                    }

                    x[i] < 0 -> x[i] % L + L
                    else -> x[i]
                }
            },
            { _, i, _, _, y, _ -> y[i] }
        ).iterator()

        var step = 0

        do {
            val state = integrator.next()
            particlesX = state.x
            particlesY = state.y
            speedsX = state.vx
            speedsY = state.vy
            particleCollisions.clear()
            obstacleCollisions.clear()
            if (step % dt2Interval == 0) {
                statesWriter.write(state)
                step = 0
            }
            particleCrossings[state.time]?.forEach(exitsWriter::writeExits)
            step++
        } while (state.time < T)
        statesWriter.close()
        exitsWriter.close()
    }

    private fun calculateCollisions(x: DoubleArray, y: DoubleArray) {
        for (i in x.indices) {
            val particleCollisionList = mutableListOf<Int>()
            for (j in x.indices) {
                if (i != j) {
                    val dx = x[i] - x[j]
                    val dxWrapped = dx - L * round(dx / L)
                    val dy = y[i] - y[j]
                    val distance = sqrt(dxWrapped.pow(2) + dy.pow(2))
                    if (distance < 2 * particleRadius) {
                        particleCollisionList.add(j)
                    }
                }
            }
            particleCollisions[i] = particleCollisionList
            val obstacleCollisionList = mutableListOf<Int>()
            for (j in obstaclesX.indices) {
                val dx = x[i] - obstaclesX[j]
                val dxWrapped = dx - L * round(dx / L)
                val dy = y[i] - obstaclesY[j]
                val distance = sqrt(dxWrapped.pow(2) + dy.pow(2))
                if (distance < obstacleRadius + particleRadius) {
                    obstacleCollisionList.add(j)
                }
            }
            obstacleCollisions[i] = obstacleCollisionList
        }
    }

    private fun calculateForces(
        i: Int,
        x: DoubleArray,
        x1: DoubleArray,
        y: DoubleArray,
        y1: DoubleArray
    ): Pair<Double, Double> {
        if (particleCollisions.isEmpty() || obstacleCollisions.isEmpty()) {
            calculateCollisions(x, y)
        }

        var f_x = 0.0
        var f_y = 0.0

        // Check collision with top wall
        if (y[i] + particleRadius >= W) {
            val superposition = y[i] + particleRadius - W

            val f_n = -k_n * superposition - gamma * y1[i] * TOP_WALL_NORM_Y  // Normal force
            val f_t = -k_t * superposition * x1[i] * TOP_WALL_TAN_X

            f_x += f_n * TOP_WALL_NORM_X + f_t * TOP_WALL_TAN_X
            f_y += f_n * TOP_WALL_NORM_Y + f_t * TOP_WALL_TAN_Y
        }

        // Check collision with bottom wall
        if (y[i] - particleRadius <= 0) {
            val superposition = particleRadius - y[i]

            val f_n = -k_n * superposition - gamma * y1[i] * BOTTOM_WALL_NORM_Y  // Normal force
            val f_t = -k_t * superposition * x1[i] * BOTTOM_WALL_TAN_X

            f_x += f_n * BOTTOM_WALL_NORM_X + f_t * BOTTOM_WALL_TAN_X
            f_y += f_n * BOTTOM_WALL_NORM_Y + f_t * BOTTOM_WALL_TAN_Y
        }

        particleCollisions[i]?.forEach {
            val dx = x[it] - x[i]
            val dxWrapped = dx - L * round(dx / L)
            val dist = sqrt((dxWrapped).pow(2) + (y[it] - y[i]).pow(2))
            val superposition = 2 * particleRadius - dist
            val relX1 = x1[i] - x1[it]
            val relY1 = y1[i] - y1[it]

            val normX = (dxWrapped) / dist
            val normY = (y[it] - y[i]) / dist
            val tanX = -normY
            val tanY = normX

            val f_n = -k_n * superposition + gamma * (normX * relX1 + normY * relY1)
            val f_t = -k_t * superposition * (tanX * relX1 + tanY * relY1)

            f_x += f_n * normX + f_t * tanX
            f_y += f_n * normY + f_t * tanY
        }

        obstacleCollisions[i]?.forEach {
            val dx = obstaclesX[it] - x[i]
            val dxWrapped = dx - L * round(dx / L)
            val dist = sqrt((dxWrapped).pow(2) + (obstaclesY[it] - y[i]).pow(2))
            val superposition = particleRadius + obstacleRadius - dist
            val relX1 = x1[i] - 0.0
            val relY1 = y1[i] - 0.0

            val normX = (dxWrapped) / dist
            val normY = (obstaclesY[it] - y[i]) / dist
            val tanX = -normY
            val tanY = normX

            val f_n = -k_n * superposition + gamma * (normX * relX1 + normY * relY1)
            val f_t = -k_t * superposition * (tanX * relX1 + tanY * relY1)

            f_x += f_n * normX + f_t * tanX
            f_y += f_n * normY + f_t * tanY
        }

        return Pair(f_x / mass + a0, f_y / mass)
    }
}