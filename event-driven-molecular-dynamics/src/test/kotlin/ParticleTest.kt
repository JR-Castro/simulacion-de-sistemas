import ar.edu.itba.ss.*
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import kotlin.math.pow
import kotlin.math.sqrt
import kotlin.test.assertNotNull
import kotlin.test.assertNull

class ParticleTest {
    private val radius = 0.1
    private val mass = 1.0

    private val distance = 2.0
    private val right = Vec2D(distance, 0.0)
    private val left = Vec2D(-distance, 0.0)
    private val up = Vec2D(0.0, distance)
    private val down = Vec2D(0.0, -distance)

    @Test
    @DisplayName("Predict head on collision")
    fun shouldCollideHeadOn() {
        val particle1 = Particle(0, -distance, 0.0, distance, 0.0, radius, mass)
        val particle2 = Particle(0, distance, 0.0, -distance, 0.0, radius, mass)
        val prediction = particle1.predictCollision(particle2)

        assertNotNull(prediction)
        assertEqualsWithTolerance(distance - radius, prediction.time * distance)
    }

    @Test
    @DisplayName("Predict 90º angle collision")
    fun shouldCollideAtAngle() {
        val particle1 = Particle(0, 0.0, distance, 0.0, -distance, radius, mass)
        val particle2 = Particle(0, -distance, 0.0, distance, 0.0, radius, mass)
        val prediction = particle1.predictCollision(particle2)

        assertNotNull(prediction)
        assertEqualsWithTolerance(distance - sqrt((2 * radius).pow(2) / 2), prediction.time * distance)
    }

    @Test
    @DisplayName("Predict no collision")
    fun shouldNotCollide() {
        val particle1 = Particle(0, -distance, 0.0, -distance, 0.0, radius, mass)
        val particle2 = Particle(0, distance, 0.0, distance, 0.0, radius, mass)
        val prediction = particle1.predictCollision(particle2)

        assertNull(prediction)
    }

    @Test
    @DisplayName("Rectilinear movement")
    fun shouldMove() {
        val particle = Particle(0, 0.0, 0.0, distance, 0.0, radius, mass)
        particle.step(1.0)

        assertEqualsWithTolerance(distance, particle.x)
    }

    @Test
    @DisplayName("No movement")
    fun shouldNotMove() {
        val particle = Particle(0, 0.0, 0.0, 0.0, 0.0, radius, mass)
        particle.step(1.0)

        assertEqualsWithTolerance(0.0, particle.x)
    }

    @Test
    @DisplayName("Collide with walls")
    fun shouldReflectVelocity() {
        val particle = Particle(0, 0.0, 0.0, 2.0, 3.0, radius, mass)

        particle.collideWithWall(WALL_RIGHT_X, WALL_RIGHT_Y)
        assertEqualsWithTolerance(-2.0, particle.vx)
        assertEqualsWithTolerance(3.0, particle.vy)

        particle.collideWithWall(WALL_TOP_X, WALL_TOP_Y)
        assertEqualsWithTolerance(-2.0, particle.vx)
        assertEqualsWithTolerance(-3.0, particle.vy)

        particle.collideWithWall(WALL_BOTTOM_X, WALL_BOTTOM_Y)
        assertEqualsWithTolerance(-2.0, particle.vx)
        assertEqualsWithTolerance(3.0, particle.vy)

        particle.collideWithWall(WALL_LEFT_X, WALL_LEFT_Y)
        assertEqualsWithTolerance(2.0, particle.vx)
        assertEqualsWithTolerance(3.0, particle.vy)
    }

    @Test
    @DisplayName("Collide with particle head on")
    fun shouldMirrorVelocity() {
        val particle1 = Particle(0, -radius, 0.0, +1.0, 0.0, radius, mass)
        val particle2 = Particle(0, +radius, 0.0, -1.0, 0.0, radius, mass)

        particle1.collideWith(particle2)

        assertEqualsWithTolerance(-1.0, particle1.vx)
        assertEqualsWithTolerance(0.0, particle1.vy)

        assertEqualsWithTolerance(+1.0, particle2.vx)
        assertEqualsWithTolerance(0.0, particle2.vy)
    }

    @Test
    @DisplayName("Collide with stationary particle")
    fun shouldExchangeVelocity() {
        val particle1 = Particle(0, -radius, 0.0, +1.0, 0.0, radius, mass)
        val particle2 = Particle(0, +radius, 0.0, 0.0, 0.0, radius, mass)

        particle1.collideWith(particle2)

        assertEqualsWithTolerance(0.0, particle1.vx)
        assertEqualsWithTolerance(0.0, particle1.vy)

        assertEqualsWithTolerance(1.0, particle2.vx)
        assertEqualsWithTolerance(0.0, particle2.vy)
    }
}
