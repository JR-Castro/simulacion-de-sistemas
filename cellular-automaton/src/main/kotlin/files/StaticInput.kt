package ar.edu.itba.ss.files

import kotlinx.serialization.Serializable

@Serializable
data class StaticInput(val areaSize: Int, val is3D: Boolean)
