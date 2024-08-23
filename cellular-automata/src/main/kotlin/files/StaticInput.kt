package ar.edu.itba.ss.files

import ar.edu.itba.ss.Rules
import kotlinx.serialization.Serializable

@Serializable
data class StaticInput(val areaSize: Int, val is3D: Boolean, val rules: Rules = Rules.CONWAY, val maxIterations: Int)
