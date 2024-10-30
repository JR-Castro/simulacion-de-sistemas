package ar.edu.itba.ss

import java.io.File

fun main() {
    val simulation =
        GranularSimulation(
            100,
            100,
            1.0,
            50.0,
            10,
            File("outputStates.csv"),
            File("outputExits.csv"),
            File("outputObstacles.csv")
        )
    simulation.run()
}