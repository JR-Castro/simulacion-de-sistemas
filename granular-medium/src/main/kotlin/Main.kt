package ar.edu.itba.ss

import java.io.File

fun main() {
    val simulation =
        GranularSimulation(
            5,
            0,
            1.0,
            20.0,
            1E-3,
            1E-2,
            File("outputStates.csv"),
            File("outputExits.csv"),
            File("outputObstacles.csv")
        )
    simulation.run()
}