package ar.edu.itba.ss

//val WALL_LEFT = Vec2D(1.0, 0.0)
val WALL_LEFT_X = 1.0
val WALL_LEFT_Y = 0.0
//val WALL_RIGHT = Vec2D(-1.0, 0.0)
val WALL_RIGHT_X = -1.0
val WALL_RIGHT_Y = 0.0
//val WALL_BOTTOM = Vec2D(0.0, 1.0)
val WALL_BOTTOM_X = 0.0
val WALL_BOTTOM_Y = 1.0
//val WALL_TOP = Vec2D(0.0, -1.0)
val WALL_TOP_X = 0.0
val WALL_TOP_Y = -1.0

class SquareContainer(sideLength: Double) : Container {
    private val wall = sideLength / 2

    override fun predictCollision(particle: Particle): ContainerCollision? {
        val horizontal = when {
            particle.vx > 0 -> ContainerCollision(
                (+wall - particle.radius - particle.x) / particle.vx,
                WALL_RIGHT_X,
                WALL_RIGHT_Y,
                particle
            )

            particle.vx < 0 -> ContainerCollision(
                (-wall + particle.radius - particle.x) / particle.vx,
                WALL_LEFT_X,
                WALL_LEFT_Y,
                particle
            )

            else -> null
        }

        val vertical = when {
            particle.vy > 0 -> ContainerCollision(
                (+wall - particle.radius - particle.y) / particle.vy,
                WALL_TOP_X,
                WALL_TOP_Y,
                particle
            )

            particle.vy < 0 -> ContainerCollision(
                (-wall + particle.radius - particle.y) / particle.vy,
                WALL_BOTTOM_X,
                WALL_BOTTOM_Y,
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
