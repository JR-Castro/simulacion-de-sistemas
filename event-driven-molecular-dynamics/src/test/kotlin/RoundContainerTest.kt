import ar.edu.itba.ss.*
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import kotlin.math.pow
import kotlin.math.sin
import kotlin.math.sqrt
import kotlin.test.assertNotNull
import kotlin.test.assertNull

class RoundContainerTest {
    val radius = 1.0
    val container = RoundContainer(radius)

    val particleRadius = 0.1
    val mass = 1.0

    @Test
    @DisplayName("Right side collision")
    fun shouldCollideRight() {
        val particle = Particle(0, Vec2D.zero(), Vec2D.unit(0.0), particleRadius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance((radius - particleRadius) / 1, prediction.time)
        assertEqualsWithTolerance(WALL_RIGHT, prediction.wallNormal)
    }

    @Test
    @DisplayName("Left side collision")
    fun shouldCollideLeft() {
        val particle = Particle(0, Vec2D.zero(), Vec2D.unit(Math.PI), particleRadius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance((radius - particleRadius) / 1, prediction.time)
        assertEqualsWithTolerance(WALL_LEFT, prediction.wallNormal)
    }

    @Test
    @DisplayName("Top side collision")
    fun shouldCollideTop() {
        val particle = Particle(0, Vec2D.zero(), Vec2D.unit(Math.PI / 2), particleRadius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance((radius - particleRadius) / 1, prediction.time)
        assertEqualsWithTolerance(WALL_TOP, prediction.wallNormal)
    }

    @Test
    @DisplayName("Bottom side collision")
    fun shouldCollideBottom() {
        val particle = Particle(0, Vec2D.zero(), Vec2D.unit(Math.PI * 3 / 2), particleRadius, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance((radius - particleRadius) / 1, prediction.time)
        assertEqualsWithTolerance(WALL_BOTTOM, prediction.wallNormal)
    }

    @Test
    @DisplayName("Lower diagonal collision")
    fun shouldCollideBottomLeft() {
        val startX = -sin(Math.PI/4)
        val particle = Particle(0, Vec2D(startX, 0.0), Vec2D(0.0, -1.0), 0.0, mass)
        val prediction = container.predictCollision(particle)

        assertNotNull(prediction)
        assertEqualsWithTolerance(sqrt((radius).pow(2) - startX.pow(2)), prediction.time)
        assertEqualsWithTolerance(Vec2D.unit(Math.PI / 4), prediction.wallNormal)
    }

    @Test
    @DisplayName("No collision")
    fun shouldNotCollide() {
        val particle = Particle(0, Vec2D.zero(), Vec2D.zero(), particleRadius, mass)
        val prediction = container.predictCollision(particle)

        assertNull(prediction)
    }

    @Test
    @DisplayName("All four corners")
    fun shouldCollideAllCorners() {
        val startX = -sin(Math.PI/4)
        val particle = Particle(0, Vec2D(startX, 0.0), Vec2D(0.0, -1.0), 0.0, mass)
        var prediction = container.predictCollision(particle)
        assertNotNull(prediction)
        assertEqualsWithTolerance(sqrt((radius).pow(2) - startX.pow(2)), prediction.time)
        assertEqualsWithTolerance(Vec2D.unit(Math.PI / 4), prediction.wallNormal)
        particle.step(prediction.time)
        particle.collideWith(prediction.wallNormal)

        prediction = container.predictCollision(particle)
        assertNotNull(prediction)
        assertEqualsWithTolerance(2 * sqrt((radius).pow(2) - startX.pow(2)), prediction.time)
        assertEqualsWithTolerance(Vec2D.unit(Math.PI * 3 / 4), prediction.wallNormal)
        particle.step(prediction.time)
        particle.collideWith(prediction.wallNormal)

        prediction = container.predictCollision(particle)
        assertNotNull(prediction)
        assertEqualsWithTolerance(2 * sqrt((radius).pow(2) - startX.pow(2)), prediction.time)
        assertEqualsWithTolerance(Vec2D.unit(Math.PI * 5 / 4), prediction.wallNormal)
        particle.step(prediction.time)
        particle.collideWith(prediction.wallNormal)

        prediction = container.predictCollision(particle)
        assertNotNull(prediction)
        assertEqualsWithTolerance(2 * sqrt((radius).pow(2) - startX.pow(2)), prediction.time)
        assertEqualsWithTolerance(Vec2D.unit(Math.PI * 7 / 4), prediction.wallNormal)
    }

}