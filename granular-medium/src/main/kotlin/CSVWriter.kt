package ar.edu.itba.ss

import java.io.Closeable
import java.io.Flushable
import java.io.Writer

class CSVWriter(private val writer: Writer) : Closeable, Flushable {

    private val SEPARATOR = ","

    init {
        writer.write("time${SEPARATOR}x${SEPARATOR}y${SEPARATOR}vx${SEPARATOR}vy\n")
    }

    fun write(xState: SimulationState, yState: SimulationState) {
        for (i in xState.speeds.indices) {
            writer.write("${xState.time}${SEPARATOR}${xState.positions[i]}${SEPARATOR}${yState.positions[i]}${SEPARATOR}${xState.speeds[i]}${SEPARATOR}${yState.speeds[i]}\n")
        }
    }

    fun writeObstacles(xPositions: DoubleArray, yPositions: DoubleArray) {
        for (i in xPositions.indices) {
            writer.write("0.0${SEPARATOR}${xPositions[i]}${SEPARATOR}${yPositions[i]}${SEPARATOR}0.0${SEPARATOR}0.0\n")
        }
    }

    override fun close() {
        writer.close()
    }

    override fun flush() {
        writer.flush()
    }
}