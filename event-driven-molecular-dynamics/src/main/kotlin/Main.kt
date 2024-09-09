package ar.edu.itba.ss

import java.nio.file.Files
import java.nio.file.Path
import java.util.PriorityQueue

data class Quadruple<A, B, C, D>(val a: A, val b: B, val c: C, val d: D)


fun processInputFiles(static_path: String, dynamic_path: String): Quadruple<String, Double, Double, List<Particle>> {
    val staticFileLines = Files.readAllLines(Path.of(static_path))
    val dynamicFileLines = Files.readAllLines(Path.of(dynamic_path))

    val layout = staticFileLines[0]
    val L = staticFileLines[1].toDouble()
    val N = staticFileLines[2].toInt()
    val T = staticFileLines[3].toDouble()

    val particles = mutableListOf<Particle>()

    for (i in 0 until N) {
        val staticPartData = staticFileLines[i + 4].split(" ")
        val dynPartData = dynamicFileLines[i + 1].split(" ")
        val x = dynPartData[1].toDouble()
        val y = dynPartData[2].toDouble()
        val vx = dynPartData[3].toDouble()
        val vy = dynPartData[4].toDouble()
        val radius = staticPartData[1].toDouble()
        val mass = staticPartData[2].toDouble()
        particles.add(Particle(i + 1, Vec2D(x, y), Vec2D(vx, vy), radius, mass))
    }

    return Quadruple(layout, L, T, particles)
}

fun main(args: Array<String>) {
    if (args.size != 3) {
        println("Usage: cmd <static_file> <dynamic_file> <output_file>")
        return
    }

    var time = 0.0
    val (layout, L, T, particles) = processInputFiles(args[0], args[1])
    val container = if (layout == "SQUARE") SquareContainer(L) else RoundContainer(L / 2)

    val collisionQueue = PriorityQueue<Collision>(compareBy { it.time })

    collisionQueue.addAll(particles
        .mapNotNull { container.predictCollision(it) })

    collisionQueue.addAll(particles
        .map { p1 -> particles.mapNotNull { p2 -> p1.predictCollision(p2) } }
        .flatten())

    val outputList: MutableList<Triple<Double, Particle, Particle?>> = mutableListOf()

    while (time < T) {
        val collision = collisionQueue.poll()
        particles.onEach { it.step(collision.time - time) }
        time = collision.time

        when (collision) {
            is ContainerCollision -> {
                collision.particle.collideWith(collision.wallNormal)

                updatePredictions(collisionQueue, particles, container, collision.particle, time)

//                val position = collision.particle.position
//                val normal = collision.wallNormal
//                println(
//                    "TIME %f: Container collision at x=%f y=%f (normal x=%f y=%f)"
//                        .format(time, position.x, position.y, normal.x, normal.y)
//                )
                outputList.add(Triple(time, collision.particle.copy(), null))
            }

            is ParticleCollision -> {
                collision.particle1.collideWith(collision.particle2)

                updatePredictions(collisionQueue, particles, container, collision.particle1, time)
                updatePredictions(collisionQueue, particles, container, collision.particle2, time)

//                val position1 = collision.particle1.position
//                val position2 = collision.particle2.position
//                println("TIME %f: Particle collision at x=%f y=%f and x=%f y=%f (distance=%f)"
//                    .format(time, position1.x, position1.y, position2.x, position2.y, (position1 - position2).modulus()))
                outputList.add(Triple(time, collision.particle1.copy(), collision.particle2.copy()))
            }
        }
    }

    Files.newBufferedWriter(Path.of(args[2])).use { file ->
        outputList.forEach {
            file.write("${it.first}")
            file.newLine()
            val part1 = it.second
            file.write("${part1.partNum} ${part1.position.x} ${part1.position.y} ${part1.velocity.x} ${part1.velocity.y}")
            file.newLine()
            if (it.third != null) {
                val particle = it.third!!
                file.write("${particle.partNum} ${particle.position.x} ${particle.position.y} ${particle.velocity.x} ${particle.velocity.y}")
                file.newLine()
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
    queue.removeIf {
        when (it) {
            is ContainerCollision -> it.particle === particle
            is ParticleCollision -> it.particle1 === particle || it.particle2 === particle
        }
    }
    queue.addAll(particles.mapNotNull { particle.predictCollision(it)?.offset(time) })
    queue.add(container.predictCollision(particle)!!.offset(time))
}
