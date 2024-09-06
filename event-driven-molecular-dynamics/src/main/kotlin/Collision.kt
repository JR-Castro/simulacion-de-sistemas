package ar.edu.itba.ss

sealed class Collision(open var time: Double) {
    fun offset(time: Double): Collision {
        this.time += time
        return this
    }
}