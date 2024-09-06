package ar.edu.itba.ss

import kotlinx.serialization.Serializable

@Serializable
data class ParticleData(
    val positionX: Double,
    val positionY: Double,
    val velocityX: Double,
    val velocityY: Double
)

@Serializable
data class SimulationStep(
    val time: Double,
    val particles: List<ParticleData>
)

@Serializable
data class SimulationData(
    val steps: Map<Double, SimulationStep>
)