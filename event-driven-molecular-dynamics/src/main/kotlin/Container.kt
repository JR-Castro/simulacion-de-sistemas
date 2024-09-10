package ar.edu.itba.ss

interface Container {
    fun predictCollision(particle: Particle): ContainerCollision?
}

data class ContainerCollision(override var time: Double, val wallNormal: Vec2D, val particle: Particle) : Collision(time) {
    private val initialCollisions = particle.collisions

    override fun isValid(): Boolean {
        return particle.collisions == initialCollisions
    }
}
