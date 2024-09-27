package ar.edu.itba.ss

import java.io.Writer

class CSVFormatter(val writer: Writer) {

    private val SEPARATOR = ","

    init {
        writer.write("time${SEPARATOR}position${SEPARATOR}speed\n")
    }

    fun write(state: SimulationState) {
        for (i in state.speeds.indices) {
            writer.write("${state.time}${SEPARATOR}${state.positions[i]}${SEPARATOR}${state.speeds[i]}\n")
        }
    }

}