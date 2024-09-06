package ar.edu.itba.ss

import java.util.PriorityQueue

fun main() {
    val L = 0.1
    val r = 0.001
    val v = 1.0
    val m = 1.0
    val N = 200
    val T = 0.5

    var time = 0.0
    val container = SquareContainer(L)
    val particles = mutableListOf<Particle>()
    while (particles.size < N) {
        val particle = Particle(Vec2D.randomInRange(-L/2 + r,L/2 - r), Vec2D.randomWithModulus(v), r, m)
        if (particles.none { (it.position - particle.position).modulus() < it.radius + particle.radius }) {
            particles.add(particle)
        }
    }

    val collisionQueue = PriorityQueue<Collision>(compareBy { it.time })

    collisionQueue.addAll(particles
        .mapNotNull { container.predictCollision(it) })

    collisionQueue.addAll(particles
        .map { p1 -> particles.mapNotNull { p2 -> p1.predictCollision(p2) } }
        .flatten())

    while (time < T) {
        val collision = collisionQueue.poll()
        particles.onEach { it.step(collision.time - time) }
        time = collision.time

        when (collision) {
            is ContainerCollision -> {
                collision.particle.collideWith(collision.wallNormal)
                
                updatePredictions(collisionQueue, particles, container, collision.particle, time)

                val position = collision.particle.position
                val normal = collision.wallNormal
                println(
                    "TIME %f: Container collision at x=%f y=%f (normal x=%f y=%f)"
                        .format(time, position.x, position.y, normal.x, normal.y)
                )
            }
            is ParticleCollision -> {
                collision.particle1.collideWith(collision.particle2)

                updatePredictions(collisionQueue, particles, container, collision.particle1, time)
                updatePredictions(collisionQueue, particles, container, collision.particle2, time)

                val position1 = collision.particle1.position
                val position2 = collision.particle2.position
                println("TIME %f: Particle collision at x=%f y=%f and x=%f y=%f (distance=%f)"
                    .format(time, position1.x, position1.y, position2.x, position2.y, (position1 - position2).modulus()))
            }
        }
    }
}

fun updatePredictions(
    queue: PriorityQueue<Collision>,
    particles: List<Particle>,
    container: Container,
    particle: Particle,
    time: Double
) {
    queue.removeIf { when (it) {
        is ContainerCollision -> it.particle === particle
        is ParticleCollision -> it.particle1 === particle || it.particle2 === particle
    } }
    queue.addAll(particles.mapNotNull { particle.predictCollision(it)?.offset(time) })
    queue.add(container.predictCollision(particle)!!.offset(time))
}
