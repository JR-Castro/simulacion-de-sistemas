package ar.edu.itba.ss

import kotlin.math.pow

class RoundContainer(val radius: Double) : Container {
    override fun predictCollision(particle: Particle): ContainerCollision? {
        val time = calculateWallCollisionTime(particle) ?: return null

        val posX = particle.x + particle.vx * time
        val posY = particle.y + particle.vy * time

        val normalX = -posX / (radius - particle.radius)
        val normalY = -posY / (radius - particle.radius)

        return ContainerCollision(time, normalX, normalY, particle)
    }

    private fun calculateWallCollisionTime(particle: Particle): Double? {
        val vx = particle.vx
        val vy = particle.vy
        val px = particle.x
        val py = particle.y

        if (vx == 0.0 && vy == 0.0) return null

        val A = vx * vx + vy * vy
        val B = 2 * (px * vx + py * vy)
        val C = px * px + py * py - (radius - particle.radius).pow(2)

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