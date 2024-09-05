package ar.edu.itba.ss

fun main() {
    val L = 0.1
    val r = 0.001
    val v = 1.0
    val m = 1.0
    val N = 200

    val container = SquareContainer(L)
    val particles = mutableListOf<Particle>()
    while (particles.size < N) {
        val particle = Particle(Vec2D.randomInRange(-L/2 + r,L/2 - r), Vec2D.randomWithModulus(v), r, m)
        if (particles.none { (it.position - particle.position).modulus() < it.radius + particle.radius }) {
            particles.add(particle)
        }
    }

    val containerCollision = particles
        .mapNotNull { container.predictCollision(it) }
        .reduce { acc, collision -> if (collision.time < acc.time) collision else acc }

    val particleCollision = particles
        .map { p1 -> particles.mapNotNull { p2 -> p1.predictCollision(p2) } }
        .flatten()
        .fold(null) { acc: ParticleCollision?, collision -> if (acc == null || collision.time < acc.time) collision else acc }

    when {
        particleCollision == null || containerCollision.time <= particleCollision.time -> {
            particles.onEach { it.step(containerCollision.time) }

            val position = containerCollision.particle.position
            println(
                "Container collision at x=%f y=%f (normal x=%f y=%f)"
                    .format(position.x, position.y)
            )
        }
        else -> {
            particles.onEach { it.step(particleCollision.time) }

            val position1 = particleCollision.particle1.position
            val position2 = particleCollision.particle2.position
            println("Particle collision at x=%f y=%f and x=%f y=%f (distance=%f)"
                .format(position1.x, position1.y, position2.x, position2.y, (position1 - position2).modulus()))
        }
    }
}
