package ar.edu.itba.ss

interface Container {
    fun predictCollision(particle: Particle): ContainerCollision?
}

data class ContainerCollision(override var time: Double, val wallNormalX: Double, val wallNormalY: Double, val particle: Particle) : Collision(time) {
    private val initialCollisions = particle.collisions

    override fun isValid(): Boolean {
        return particle.collisions == initialCollisions
    }
}
