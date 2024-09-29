package ar.edu.itba.ss

import java.io.Closeable
import java.io.Flushable
import java.io.Writer

class CSVWriter(private val writer: Writer): Closeable, Flushable {

    private val SEPARATOR = ","

    init {
        writer.write("time${SEPARATOR}position${SEPARATOR}speed\n")
    }

    fun write(state: SimulationState) {
        for (i in state.speeds.indices) {
            writer.write("${state.time}${SEPARATOR}${state.positions[i]}${SEPARATOR}${state.speeds[i]}\n")
        }
    }

    override fun close() {
        writer.close()
    }

    override fun flush() {
        writer.flush()
    }
}