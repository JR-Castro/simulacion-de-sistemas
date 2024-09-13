package ar.edu.itba.ss

import java.io.BufferedWriter
import java.nio.file.Files
import java.nio.file.Path
import java.util.PriorityQueue

data class Quintuple<A, B, C, D, E>(val a: A, val b: B, val c: C, val d: D, val e: E)


fun processInputFiles(static_path: String, dynamic_path: String): Quintuple<String, Double, Double, Double, List<Particle>> {
    val staticFileLines = Files.readAllLines(Path.of(static_path))
    val dynamicFileLines = Files.readAllLines(Path.of(dynamic_path))

    val layout = staticFileLines[0]
    val L = staticFileLines[1].toDouble()
    val N = staticFileLines[2].toInt()
    val T = staticFileLines[3].toDouble()
    val outputStep = staticFileLines[4].toDouble()

    val particles = mutableListOf<Particle>()

    for (i in 0 until N) {
        val staticPartData = staticFileLines[i + 5].split(" ")
        val dynPartData = dynamicFileLines[i + 1].split(" ")
        val x = dynPartData[1].toDouble()
        val y = dynPartData[2].toDouble()
        val vx = dynPartData[3].toDouble()
        val vy = dynPartData[4].toDouble()
        val radius = staticPartData[1].toDouble()
        val mass = if (staticPartData[2] == "inf") Double.POSITIVE_INFINITY else staticPartData[2].toDouble()
        particles.add(Particle(i + 1, x, y, vx, vy, radius, mass))
    }

    return Quintuple(layout, L, T, outputStep, particles)
}

fun main(args: Array<String>) {
    if (args.size != 3) {
        println("Usage: cmd <static_file> <dynamic_file> <output_file>")
        return
    }

    var time = 0.0
    val (layout, L, T, outputStep, particles) = processInputFiles(args[0], args[1])
    val container = if (layout == "SQUARE") SquareContainer(L) else RoundContainer(L / 2)

    val collisionQueue = PriorityQueue<Collision>()
    collisionQueue.addAll(particles
        .mapNotNull { container.predictCollision(it) })
    collisionQueue.addAll(particles
        .map { p1 -> particles.mapNotNull { p2 -> p1.predictCollision(p2) } }
        .flatten())

    val collisionsList: MutableList<Triple<Double, Particle, Particle?>> = mutableListOf()
    val statesList: MutableList<Pair<Double, List<Particle>>> = mutableListOf()
    statesList.add(Pair(time, particles.map { it.copy() }))

    val collisionsWriter = Files.newBufferedWriter(Path.of(args[2] + "_collisions.txt"))
    val statesWriter = Files.newBufferedWriter(Path.of(args[2] + "_states.txt"))


    val startTime = System.currentTimeMillis()
    var lastStateOutputTime = 0.0

    while (time < T) {

        if (time - lastStateOutputTime >= outputStep) {
            statesList.add(Pair(time, particles.map { it.copy() }))
            lastStateOutputTime = time
        }

        if (collisionQueue.size > 50000) {
            collisionQueue.removeIf { !it.isValid() }
        }

        if (collisionsList.size > 100000 || statesList.size > 10000) {
            writeOutput(collisionsWriter, statesWriter, collisionsList, statesList)
            collisionsList.clear()
            statesList.clear()
        }

        val collision = getFirstValid(collisionQueue) ?: break

        particles.onEach { it.step(collision.time - time) }
        time = collision.time

        print("\r$time")

        when (collision) {
            is ContainerCollision -> {
                collision.particle.collideWithWall(collision.wallNormalX, collision.wallNormalY)

                updatePredictions(collisionQueue, particles, container, collision.particle, time)

                collisionsList.add(Triple(time, collision.particle.copy(), null))
            }

            is ParticleCollision -> {
                collision.particle1.collideWith(collision.particle2)

                updatePredictionsTwoParticles(
                    collisionQueue,
                    particles,
                    container,
                    collision.particle1,
                    collision.particle2,
                    time
                )

                collisionsList.add(Triple(time, collision.particle1.copy(), collision.particle2.copy()))
            }
        }
    }

    println("\rElapsed time: ${System.currentTimeMillis() - startTime} ms")

    writeOutput(collisionsWriter, statesWriter, collisionsList, statesList)

    collisionsWriter.close()
    statesWriter.close()
}

fun writeOutput(
    collisionsWriter: BufferedWriter,
    statesWriter: BufferedWriter,
    collisionsList: List<Triple<Double, Particle, Particle?>>,
    statesList: List<Pair<Double, List<Particle>>>
) {
    collisionsList.forEach {
        collisionsWriter.write("${it.first}")
        if (it.third != null) {
            // indicate there were two particles
            collisionsWriter.write(" 2\n")
            val part1 = it.second
            collisionsWriter.write("${part1.partNum} ${part1.x} ${part1.y} ${part1.x} ${part1.y}\n")
            val particle = it.third!!
            collisionsWriter.write("${particle.partNum} ${particle.x} ${particle.y} ${particle.x} ${particle.y}\n")
        } else {
            collisionsWriter.write(" 1\n")
            val part1 = it.second
            collisionsWriter.write("${part1.partNum} ${part1.x} ${part1.y} ${part1.x} ${part1.y}\n")
        }
    }
    for ((time, particles) in statesList) {
        statesWriter.write("$time")
        statesWriter.newLine()
        particles.forEach {
            statesWriter.write("${it.partNum} ${it.x} ${it.y} ${it.vx} ${it.vy}\n")
        }
    }
}

fun getFirstValid(
    collisionQueue: PriorityQueue<Collision>
): Collision? {
    while (collisionQueue.isNotEmpty() && !collisionQueue.peek().isValid()) {
        collisionQueue.poll()
    }

    if (collisionQueue.isEmpty()) {
        return null
    }

    return collisionQueue.poll()
}

fun updatePredictions(
    queue: PriorityQueue<Collision>,
    particles: List<Particle>,
    container: Container,
    particle: Particle,
    time: Double
) {
    queue.addAll(particles.mapNotNull { particle.predictCollision(it)?.offset(time) })
    val collision = container.predictCollision(particle)
    if (collision != null) {
        queue.add(collision.offset(time))
    }
}

fun updatePredictionsTwoParticles(
    queue: PriorityQueue<Collision>,
    particles: List<Particle>,
    container: Container,
    partticle1: Particle,
    particle2: Particle,
    time: Double
) {
    queue.addAll(particles.mapNotNull { partticle1.predictCollision(it)?.offset(time) })
    queue.addAll(particles.mapNotNull { particle2.predictCollision(it)?.offset(time) })
    val collision1 = container.predictCollision(partticle1)
    if (collision1 != null) {
        queue.add(collision1.offset(time))
    }
    val collision2 = container.predictCollision(particle2)
    if (collision2 != null) {
        queue.add(collision2.offset(time))
    }
}
