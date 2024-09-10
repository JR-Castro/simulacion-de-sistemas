package ar.edu.itba.ss

sealed class Collision(open var time: Double): Comparable<Collision> {
    fun offset(time: Double): Collision {
        this.time += time
        return this
    }

    override fun compareTo(other: Collision): Int = time compareTo other.time

    abstract fun isValid(): Boolean
}