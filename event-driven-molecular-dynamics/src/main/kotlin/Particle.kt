package ar.edu.itba.ss

import kotlin.math.pow
import kotlin.math.sqrt

data class Particle(
    val partNum: Int,
    var x: Double, var y: Double,  // Position (x, y)
    var vx: Double, var vy: Double,  // Velocity (vx, vy)
    val radius: Double,
    val mass: Double
) {
    var collisions = 0

    fun predictCollision(particle: Particle): ParticleCollision? {
        val deltaX = particle.x - this.x
        val deltaY = particle.y - this.y
        val deltaVX = particle.vx - this.vx
        val deltaVY = particle.vy - this.vy

        val deltaRDotDeltaV = deltaX * deltaVX + deltaY * deltaVY
        if (deltaRDotDeltaV >= 0) return null

        val sigma = particle.radius + this.radius
        val deltaRSq = deltaX * deltaX + deltaY * deltaY
        val deltaVSq = deltaVX * deltaVX + deltaVY * deltaVY
        val d = deltaRDotDeltaV.pow(2) - deltaVSq * (deltaRSq - sigma.pow(2))

        if (d < 0) return null

        return ParticleCollision(
            - (deltaRDotDeltaV + sqrt(d)) / deltaVSq,
            this,
            particle
        )
    }

    fun step(time: Double) {
        x += vx * time
        y += vy * time
    }

    fun collideWithWall(wallNormalX: Double, wallNormalY: Double) {
        val dotProduct = vx * wallNormalX + vy * wallNormalY
        vx -= 2.0 * dotProduct * wallNormalX
        vy -= 2.0 * dotProduct * wallNormalY
        collisions += 1
    }

    fun collideWith(particle: Particle) {
        val deltaX = particle.x - this.x
        val deltaY = particle.y - this.y
        val deltaVX = particle.vx - this.vx
        val deltaVY = particle.vy - this.vy
        val sigma = particle.radius + this.radius

        val deltaRDotDeltaV = deltaX * deltaVX + deltaY * deltaVY

        // Handle the case when one particle has infinite mass (i.e., a fixed obstacle)
        if (this.mass == Double.POSITIVE_INFINITY) {
            // Only the other particle's velocity changes
            val j = (2.0 * particle.mass * deltaRDotDeltaV) / (sigma * particle.mass)

            val jx = (deltaX * j) / sigma
            val jy = (deltaY * j) / sigma

            particle.vx -= jx / particle.mass
            particle.vy -= jy / particle.mass
        } else if (particle.mass == Double.POSITIVE_INFINITY) {
            // Only this particle's velocity changes
            val j = (2.0 * this.mass * deltaRDotDeltaV) / (sigma * this.mass)

            val jx = (deltaX * j) / sigma
            val jy = (deltaY * j) / sigma

            this.vx += jx / this.mass
            this.vy += jy / this.mass
        } else {
            // Regular case: both particles move
            val j = (2.0 * this.mass * particle.mass * deltaRDotDeltaV) / (sigma * (this.mass + particle.mass))

            val jx = (deltaX * j) / sigma
            val jy = (deltaY * j) / sigma

            this.vx += jx / this.mass
            this.vy += jy / this.mass
            particle.vx -= jx / particle.mass
            particle.vy -= jy / particle.mass
        }

        collisions += 1
        particle.collisions += 1
    }
}

data class ParticleCollision(
    override var time: Double,
    val particle1: Particle,
    val particle2: Particle
) : Collision(time) {

    private val initialCollisions1 = particle1.collisions
    private val initialCollisions2 = particle2.collisions

    override fun isValid(): Boolean {
        return particle1.collisions == initialCollisions1 && particle2.collisions == initialCollisions2
    }
}
