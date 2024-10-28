package ar.edu.itba.ss

import java.io.Closeable
import java.io.Flushable
import java.io.Writer

class CSVWriter(private val writer: Writer) : Closeable, Flushable {

    private val SEPARATOR = ","

    init {
        writer.write("time${SEPARATOR}x${SEPARATOR}y${SEPARATOR}vx${SEPARATOR}vy\n")
    }

    fun write(state: SimulationState) {
        for (i in state.x.indices) {
            writer.write("${state.time}${SEPARATOR}${state.x[i]}${SEPARATOR}${state.y[i]}${SEPARATOR}${state.vx[i]}${SEPARATOR}${state.vy[i]}\n")
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