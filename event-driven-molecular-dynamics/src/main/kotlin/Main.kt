package ar.edu.itba.ss

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

    while (time < T) {
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
                containerCollision.particle.collideWith(containerCollision.wallNormal)
                time += containerCollision.time

                val position = containerCollision.particle.position
                val normal = containerCollision.wallNormal
                println(
                    "TIME %f: Container collision at x=%f y=%f (normal x=%f y=%f)"
                        .format(time, position.x, position.y, normal.x, normal.y)
                )
            }
            else -> {
                particles.onEach { it.step(particleCollision.time) }
                particleCollision.particle1.collideWith(particleCollision.particle2)
                time += particleCollision.time

                val position1 = particleCollision.particle1.position
                val position2 = particleCollision.particle2.position
                println("TIME %f: Particle collision at x=%f y=%f and x=%f y=%f (distance=%f)"
                    .format(time, position1.x, position1.y, position2.x, position2.y, (position1 - position2).modulus()))
            }
        }
    }
}
