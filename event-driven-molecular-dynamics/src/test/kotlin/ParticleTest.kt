import ar.edu.itba.ss.Particle
import ar.edu.itba.ss.Vec2D
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
    private val up =   Vec2D(0.0, distance)
    private val down = Vec2D(0.0, -distance)

    @Test
    @DisplayName("Head on collision")
    fun shouldCollideHeadOn() {
        val particle1 = Particle(left, right, radius, mass)
        val particle2 = Particle(right, left, radius, mass)
        val prediction = particle1.predictCollision(particle2)

        assertNotNull(prediction)
        assertEqualsWithTolerance(distance - radius, prediction.time * distance)
    }

    @Test
    @DisplayName("90º angle collision")
    fun shouldCollideAtAngle() {
        val particle1 = Particle(up, down, radius, mass)
        val particle2 = Particle(left, right, radius, mass)
        val prediction = particle1.predictCollision(particle2)

        assertNotNull(prediction)
        assertEqualsWithTolerance(distance - sqrt((2*radius).pow(2) / 2), prediction.time * distance)
    }

    @Test
    @DisplayName("No collision")
    fun shouldNotCollide() {
        val particle1 = Particle(left, left, radius, mass)
        val particle2 = Particle(right, right, radius, mass)
        val prediction = particle1.predictCollision(particle2)

        assertNull(prediction)
    }
}
