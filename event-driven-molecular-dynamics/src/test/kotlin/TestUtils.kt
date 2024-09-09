import ar.edu.itba.ss.Vec2D
import kotlin.test.assertEquals

private const val EPSILON = 1.0e-14

fun assertEqualsWithTolerance(expected: Double, actual: Double) {
    assertEquals(expected, actual, EPSILON)
}

fun assertEqualsWithTolerance(expected: Vec2D, actual: Vec2D) {
    assertEquals(expected.x, actual.x, EPSILON)
    assertEquals(expected.y, actual.y, EPSILON)
}
