package ar.edu.itba.ss

import kotlin.math.pow
import kotlin.math.sqrt

data class Particle(var position: Vec2D, val velocity: Vec2D, val radius: Double, val mass: Double) {
    fun predictCollision(particle: Particle): ParticleCollision? {
        val deltaR = this.position - particle.position
        val deltaV = this.velocity - particle.velocity

        if (deltaV * deltaR >= 0) return null

        val sigma = this.radius + particle.radius
        val d = (deltaV * deltaR).pow(2) - (deltaV * deltaV) * (deltaR * deltaR - sigma.pow(2))

        if (d < 0) return null

        return ParticleCollision(- (deltaV * deltaR + sqrt(d)) / (deltaV * deltaV), this, particle)
    }

    fun step(time: Double) {
        position += velocity * time
    }
}

data class ParticleCollision(val time: Double, val particle1: Particle, val particle2: Particle)
