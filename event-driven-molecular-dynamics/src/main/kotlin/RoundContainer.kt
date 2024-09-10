package ar.edu.itba.ss

import kotlin.math.pow

class RoundContainer(val radius: Double) : Container {
    override fun predictCollision(particle: Particle): ContainerCollision? {
        val time = calculateWallCollisionTime(particle) ?: return null

        val pos = particle.position + particle.velocity * time

        val normal = -pos / (radius - particle.radius)

        return ContainerCollision(time, normal, particle)
    }

    private fun calculateWallCollisionTime(particle: Particle): Double? {
        val velocity = particle.velocity
        val position = particle.position

        if (velocity.x == 0.0 && velocity.y == 0.0) return null

        val A = velocity.normSq()
        val B = 2 * (particle.position * particle.velocity)
        val C = position.normSq() - (radius - particle.radius).pow(2)

        val discriminant = B * B - 4 * A * C

        if (discriminant < 0) return null

        val sqrtDisc = kotlin.math.sqrt(discriminant)
        val t1 = (-B + sqrtDisc) / (2 * A)
        val t2 = (-B - sqrtDisc) / (2 * A)

        val min = minOf(t1, t2)

        return when {
            min > 0 -> min
            t1 <= 0.0 && t2 > 0.0 -> t2
            t1 > 0.0 && t2 <= 0.0 -> t1
            else -> null
        }
    }
}