import ar.edu.itba.ss.Vec2D
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import kotlin.math.pow
import kotlin.math.sqrt
import kotlin.test.assertEquals

class Vec2DTest {
    private val vec1 = Vec2D(3.0, 5.0)
    private val vec2 = Vec2D(1.0, 2.0)
    private val num = 2.0

    private val sum = Vec2D(4.0, 7.0)
    private val diff = Vec2D(2.0, 3.0)
    private val dot = 13.0
    private val scalar = Vec2D(6.0, 10.0)
    private val modulus = sqrt(3.0.pow(2) + 5.0.pow(2))

    @Test
    @DisplayName("Vector addition")
    fun shouldReturnSum() {
        val sum = vec1 + vec2

        assertEqualsWithTolerance(this.sum, sum)
    }

    @Test
    @DisplayName("Vector subtraction")
    fun shouldReturnDifference() {
        val diff = vec1 - vec2

        assertEqualsWithTolerance(this.diff, diff)
    }

    @Test
    @DisplayName("Vector dot product")
    fun shouldReturnDotProduct() {
        val dot = vec1 * vec2

        assertEqualsWithTolerance(this.dot, dot)
    }

    @Test
    @DisplayName("Vector scalar product")
    fun shouldReturnScalarProduct() {
        val scalar = vec1 * num

        assertEqualsWithTolerance(this.scalar, scalar)
    }

    @Test
    @DisplayName("Vector modulus")
    fun shouldReturnModulus() {
        val modulus = vec1.modulus()

        assertEqualsWithTolerance(this.modulus, modulus)
    }

    @Test
    @DisplayName("Vector zero")
    fun shouldReturnZero() {
        val zero = Vec2D.zero()

        assertEquals(Vec2D(0.0, 0.0), zero)
    }

    @Test
    @DisplayName("Vector unit 0º")
    fun shouldReturnUnitRight() {
        val unit = Vec2D.unit(0.0)

        assertEqualsWithTolerance(Vec2D(1.0, 0.0), unit)
    }

    @Test
    @DisplayName("Vector unit 90º")
    fun shouldReturnUnitUp() {
        val unit = Vec2D.unit(Math.PI / 2)

        assertEqualsWithTolerance(Vec2D(0.0, 1.0), unit)
    }

    @Test
    @DisplayName("Vector unit 180º")
    fun shouldReturnUnitLeft() {
        val unit = Vec2D.unit(Math.PI)

        assertEqualsWithTolerance(Vec2D(-1.0, 0.0), unit)
    }

    @Test
    @DisplayName("Vector unit 270º")
    fun shouldReturnUnitDown() {
        val unit = Vec2D.unit(Math.PI * 3 / 2)

        assertEqualsWithTolerance(Vec2D(0.0, -1.0), unit)
    }

    @Test
    @DisplayName("Vector unit 360º")
    fun shouldReturnUnitLoop() {
        val unit = Vec2D.unit(Math.PI * 2)

        assertEqualsWithTolerance(Vec2D(1.0, 0.0), unit)
    }

    @Test
    @DisplayName("Mirror vector with surface normal")
    fun shouldReturnMirrored() {
        val vec = Vec2D(2.0, 3.0)
        val normal = Vec2D(1.0, 0.0)

        val mirrored = vec - normal * (normal * vec) * 2.0

        assertEqualsWithTolerance(Vec2D(-2.0, 3.0), mirrored)
    }
}
