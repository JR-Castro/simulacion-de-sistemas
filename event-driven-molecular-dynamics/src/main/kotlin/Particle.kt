package ar.edu.itba.ss

import kotlin.math.pow
import kotlin.math.sqrt

data class Particle(val partNum: Int, var position: Vec2D, var velocity: Vec2D, val radius: Double, val mass: Double) {
    fun predictCollision(particle: Particle): ParticleCollision? {
        val deltaR = particle.position - this.position
        val deltaV = particle.velocity - this.velocity

        if (deltaV * deltaR >= 0) return null

        val sigma = particle.radius + this.radius
        val d = (deltaV * deltaR).pow(2) - (deltaV * deltaV) * (deltaR * deltaR - sigma.pow(2))

        if (d < 0) return null

        return ParticleCollision(- (deltaV * deltaR + sqrt(d)) / (deltaV * deltaV), this, particle)
    }

    fun step(time: Double) {
        position += velocity * time
    }

    fun collideWith(wallNormal: Vec2D) {
        velocity -= wallNormal * (wallNormal * velocity) * 2.0
    }

    fun collideWith(particle: Particle) {
        val deltaR = particle.position - this.position
        val deltaV = particle.velocity - this.velocity
        val sigma = particle.radius + this.radius

        val j = (2.0 * this.mass * particle.mass * (deltaV * deltaR)) / (sigma * (this.mass + particle.mass))

        val jVec = (deltaR * j) / sigma

        this.velocity += jVec / this.mass
        particle.velocity -= jVec / particle.mass
    }
}

data class ParticleCollision(override var time: Double, val particle1: Particle, val particle2: Particle) : Collision(time)
