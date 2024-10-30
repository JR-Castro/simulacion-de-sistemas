package ar.edu.itba.ss

import java.io.File

fun main() {
    val simulation =
        GranularSimulation(
            1,
            0,
            1.0,
            20.0,
            3,
            File("outputStates.csv"),
            File("outputExits.csv"),
            File("outputObstacles.csv")
        )
    simulation.run()
}