package ar.edu.itba.ss

val WALL_LEFT = Vec2D(1.0, 0.0)
val WALL_RIGHT = Vec2D(-1.0, 0.0)
val WALL_BOTTOM = Vec2D(0.0, 1.0)
val WALL_TOP = Vec2D(0.0, -1.0)

class SquareContainer(sideLength: Double) : Container {
    private val wall = sideLength / 2

    override fun predictCollision(particle: Particle): ContainerCollision? {
        val horizontal = when {
            particle.velocity.x > 0 -> ContainerCollision(
                (+wall - particle.radius - particle.position.x) / particle.velocity.x,
                WALL_RIGHT,
                particle
            )

            particle.velocity.x < 0 -> ContainerCollision(
                (-wall + particle.radius - particle.position.x) / particle.velocity.x,
                WALL_LEFT,
                particle
            )

            else -> null
        }
        val vertical = when {
            particle.velocity.y > 0 -> ContainerCollision(
                (+wall - particle.radius - particle.position.y) / particle.velocity.y,
                WALL_TOP,
                particle
            )

            particle.velocity.y < 0 -> ContainerCollision(
                (-wall + particle.radius - particle.position.y) / particle.velocity.y,
                WALL_BOTTOM,
                particle
            )

            else -> null
        }

        return when {
            horizontal == null && vertical == null -> null
            vertical != null && (horizontal == null || vertical.time <= horizontal.time) && vertical.time > 0 -> vertical
            horizontal != null && horizontal.time > 0 -> horizontal
            else -> null
        }
    }
}
