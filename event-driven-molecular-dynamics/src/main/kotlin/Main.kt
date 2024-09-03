package ar.edu.itba.ss

import kotlin.time.measureTime

fun main() {
    val L = 0.1
    val r = 0.001
    val v = 1.0
    val m = 1.0
    val N = 1000

    val container = SquareContainer(L)
    val particles = mutableListOf<Particle>()
    while (particles.size < N) {
        val particle = Particle(Vec2D.randomInRange(-L/2 + r,L/2 - r), Vec2D.randomWithModulus(v), r, m)
        if (particles.none { (it.position - particle.position).modulus() < it.radius + particle.radius }) {
            particles.add(particle)
        }
    }

    println(measureTime {
        particles
            .mapNotNull { container.predictCollision(it) }
            .reduce { acc, collision -> if (collision.time < acc.time) collision else acc }
    })

    println(measureTime {
        particles
            .map { p1 -> particles.mapNotNull { p2 -> p1.predictCollision(p2) } }
            .flatten()
            .fold(null) { acc: ParticleCollision?, collision -> if (acc == null || collision.time < acc.time) collision else acc }
    })
}
