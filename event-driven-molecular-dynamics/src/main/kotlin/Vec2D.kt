package ar.edu.itba.ss

import kotlin.math.cos
import kotlin.math.pow
import kotlin.math.sin
import kotlin.math.sqrt
import kotlin.random.Random

data class Vec2D(val x: Double, val y: Double) {
    operator fun plus(vec2D: Vec2D): Vec2D {
        return Vec2D(x + vec2D.x, y + vec2D.y)
    }

    operator fun minus(vec2D: Vec2D): Vec2D {
        return Vec2D(x - vec2D.x, y - vec2D.y)
    }

    operator fun times(vec2D: Vec2D): Double {
        return x * vec2D.x + y * vec2D.y
    }

    operator fun times(scalar: Double): Vec2D {
        return Vec2D(this.x * scalar, this.y * scalar)
    }

    fun modulus(): Double {
        return sqrt(this.x.pow(2) + this.y.pow(2))
    }

    companion object {
        fun zero(): Vec2D {
            return Vec2D(0.0, 0.0)
        }

        fun unit(angle: Double): Vec2D {
            return Vec2D(cos(angle), sin(angle))
        }

        fun randomInRange(from: Double, until: Double): Vec2D {
            return Vec2D(Random.nextDouble(from, until), Random.nextDouble(from, until))
        }

        fun randomWithModulus(modulus: Double): Vec2D {
            return unit(Random.nextDouble(Math.PI * 2)) * modulus
        }
    }
}
