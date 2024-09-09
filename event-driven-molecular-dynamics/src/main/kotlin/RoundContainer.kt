package ar.edu.itba.ss

import kotlin.math.pow

class RoundContainer(val radius: Double) : Container {
    override fun predictCollision(particle: Particle): ContainerCollision? {
        val time = calculateWallCollisionTime(particle) ?: return null

        val pos = particle.position + particle.velocity * time


        val normal = - pos / (radius - particle.radius)

        return ContainerCollision(time, normal, particle)
    }

    private fun calculateWallCollisionTime(particle: Particle): Double? {
        if (particle.velocity.x == 0.0 && particle.velocity.y == 0.0) return null

        val A = particle.velocity.x.pow(2) + particle.velocity.y.pow(2)
        val B = 2 * (particle.position * particle.velocity)
        val C = particle.position.x.pow(2) + particle.position.y.pow(2) - (radius - particle.radius).pow(2)

        val discriminant = B.pow(2) - 4 * A * C

        if (discriminant < 0) return null

        val t1 = (-B + kotlin.math.sqrt(discriminant)) / (2 * A)
        val t2 = (-B - kotlin.math.sqrt(discriminant)) / (2 * A)

        return if (t1 < 0.0 && t2 < 0.0) null
        else if (t1 <= 0.0 && t2 > 0.0) t2
        else if (t1 > 0.0 && t2 <= 0.0) t1
        else if (t1 < t2) t1
        else t2
    }
}