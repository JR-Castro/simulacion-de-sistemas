import ar.edu.itba.ss.Vec2D
import kotlin.math.abs

private const val EPSILON = 1.0e-14

fun assertEqualsWithTolerance(expected: Double, actual: Double) {
    assert(abs(actual - expected) < EPSILON)
}

fun assertEqualsWithTolerance(expected: Vec2D, actual: Vec2D) {
    val diff = actual - expected
    assert(abs(diff.x) < EPSILON && abs(diff.y) < EPSILON)
}
