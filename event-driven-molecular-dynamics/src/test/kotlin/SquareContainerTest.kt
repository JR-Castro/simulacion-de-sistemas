import ar.edu.itba.ss.*
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull
import kotlin.test.assertNull

class SquareContainerTest {
    private val sideLength = 2.0
    private val container = SquareContainer(sideLength)

    private val radius = 0.1
    private val mass = 1.0

    @Test
    @DisplayName("Right side collision")
    fun shouldCollideRight() {
        val particle = Particle(Vec2D.zero(), Vec2D.unit(0.0), radius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance(1.0 - radius, prediction.time)
        assertEquals(WALL_RIGHT, prediction.wallNormal)
    }

    @Test
    @DisplayName("Left side collision")
    fun shouldCollideLeft() {
        val particle = Particle(Vec2D.zero(), Vec2D.unit(Math.PI), radius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance(1.0 - radius, prediction.time)
        assertEquals(WALL_LEFT, prediction.wallNormal)
    }

    @Test
    @DisplayName("Top side collision")
    fun shouldCollideTop() {
        val particle = Particle(Vec2D.zero(), Vec2D.unit(Math.PI / 2), radius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance(1.0 - radius, prediction.time)
        assertEquals(WALL_TOP, prediction.wallNormal)
    }

    @Test
    @DisplayName("Bottom side collision")
    fun shouldCollideBottom() {
        val particle = Particle(Vec2D.zero(), Vec2D.unit(Math.PI * 3 / 2), radius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance(1.0 - radius, prediction.time)
        assertEquals(WALL_BOTTOM, prediction.wallNormal)
    }

    @Test
    @DisplayName("No collision")
    fun shouldNotCollide() {
        val particle = Particle(Vec2D.zero(), Vec2D.zero(), radius, mass)
        val prediction = container.predictCollision(particle)

        assertNull(prediction)
    }
}
