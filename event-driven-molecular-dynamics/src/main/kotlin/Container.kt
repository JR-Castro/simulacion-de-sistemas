package ar.edu.itba.ss

interface Container {
    fun predictCollision(particle: Particle): ContainerCollision?
}

data class ContainerCollision(val time: Double, val wallNormal: Vec2D, val particle: Particle)
