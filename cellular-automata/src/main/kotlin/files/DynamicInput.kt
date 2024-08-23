package ar.edu.itba.ss.files

import kotlinx.serialization.EncodeDefault
import kotlinx.serialization.Serializable

@Serializable
data class DynamicInput(val moments: List<DynamicInputState>)

@Serializable
data class DynamicInputState(val time: Int, val cells: List<DynamicInputCell>)

@Serializable
data class DynamicInputCell(val x: Int, val y: Int, val z: Int = 0, @EncodeDefault val state: Int = 0)
