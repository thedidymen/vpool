
from vpython import *

# Sizes in tenths of milimeters
table_typen = {
    "Biljart": {
        "match": {
            "height": 28400,
            "width": 14200,
            "acquit": 1825,
            "cushion": 370,
        },
        "club": {
            "height": 23000,
            "width": 11500,
            "acquit": 1550,
            "cushion": 370,
        },
        "cafe": {
            "height": 21000,
            "width": 10500,
            "acquit": 1375,
            "cushion": 370,
        },
        "oefen": {
            "height": 18000,
            "width": 9000,
            "acquit": 1175,
            "cushion": 370,
        },
        "holes": {
            "present": False,
        }
    },
    "Pool": {
        # Rail height = 63,5 % of ball height
        # https://wpapool.com/equipment-specifications/#Rail-and-Cushion
        "match": {
            "height": 25400,
            "width": 12700,
        },
        "club": {
            "height": 22368,
            "width": 11684,
        },
        "cafe": {
            "height": 19304,
            "width": 9652,
        },
        "holes": {
            "present": True,
        }
    },
    "Snooker": {
        "match": {
            "height": 35690,
            "width": 17780,
        },
        "holes": {
            "present": True,
        }
    },
}

# games = {
#     "Libre": {
#         "start_pos": {
#             "White": {
#                 "color": vector(.8, .8, .8),
#                 "location": vector()
#             }
#         }
#     }
# }

# Sizes in tenths of milimeters
ballen_typen = {
    "Biljart": {
        "size": 615 // 2
    },
    "Pool": {
        "size": 572/2
    },
    "Snooker": {
        "size": 524/2
    },
}

class Table:

    def __init__(self, height, width, cushion, holes=False) -> None:
        self.cushion = cushion
        self.height = height
        self.width = width
        self.holes = holes
        self.color_green = vector(118/255,238/255, 0)
        self.color_wood = vector(133/255, 94/255, 66/255)
        self.table = self.create_table()

    def create_table(self):
        ground = box(size=vector(self.height + self.cushion, 1, self.width + self.cushion), pos=vector(0, -1, 0), color=self.color_green)
        
        wall_a = box(pos=vector(0, self.cushion // 2, -(self.width + self.cushion) // 2), axis=vector(1, 0, 0), size=vector(self.height + 1.65 * self.cushion, self.cushion, self.cushion), color=self.color_green)
        wall_b = box(pos=vector(-(self.height + self.cushion) // 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 1.65 * self.cushion, self.cushion, self.cushion), color=self.color_green)
        wall_c = box(pos=vector(0, self.cushion // 2, (self.width + self.cushion) // 2), axis=vector(1, 0, 0), size=vector(self.height + 1.65 * self.cushion, self.cushion, self.cushion), color=self.color_green)  
        wall_d = box(pos=vector((self.height + self.cushion) // 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 1.65 * self.cushion, self.cushion, self.cushion), color=self.color_green)   
        
        wall_a.rotate(angle=pi/11.)
        wall_b.rotate(angle=-pi/11.)
        wall_c.rotate(angle=-pi/11.)
        wall_d.rotate(angle=pi/11.)

        bound_a = box(pos=vector(0, self.cushion // 2, -(self.width + 4.75 * self.cushion) // 2), axis=vector(1, 0, 0), size=vector(self.height + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.color_wood)
        bound_b = box(pos=vector(-(self.height + 4.75 * self.cushion)// 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.color_wood)
        bound_c = box(pos=vector(0, self.cushion // 2, (self.width + 4.75 * self.cushion) //2), axis=vector(1, 0, 0), size=vector(self.height + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.color_wood)  
        bound_d = box(pos=vector((self.height + 4.75 * self.cushion) // 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.color_wood)   

        objects = [wall_a, wall_b, wall_c, wall_d, bound_a, bound_b, bound_c, bound_d]
        # return compound(objects, pos=vector(0,0,0))

    def get_short_cushion(self):
        """Return location of short cushion."""
        # TO DO: figure out why to multiply by .5 to make the balls touch th cushion.
        return (self.width - 0.5 * self.cushion) // 2

    def get_long_cushion(self):
        """Return location of long cushion."""
        # TO DO: figure out why to multiply by .5 to make the balls touch th cushion.
        return (self.height - 0.5 * self.cushion) // 2


class Ball:

    def __init__(self, radius, color, location, dt) -> None:
        """Create a ball with a radius, color and location. dT is the time interval for each update."""
        self.dt = dt
        self.radius = radius
        self.ball = sphere(radius=radius, pos=location, color=color)
        self.ball.vel = vector(-3000, 0, 3000)

    def update(self, direction=1):
        """Updat ball position with its velocity multiplied by delta T for directions times. Negative directions reverses steps."""
        self.ball.pos = self.ball.pos + self.ball.vel * self.dt * direction

    def get_position(self):
        """Get ball positions"""
        return self.ball.pos

    def get_velocity(self):
        """Get ball velocity"""
        return self.ball.vel

    def set_velocity(self, vel):
        self.ball.vel = vel

    def get_radius(self):
        """Get ball radius"""
        return self.radius

    def invert_z_velocity(self):
        """Invert the z component of the velocity"""
        self.ball.vel.z *= -1.0

    def invert_x_velocity(self):
        """Invert the x component of the velocity"""
        self.ball.vel.x *= -1.0


class Collision:

    def __init__(self, table, ball):
        self.table = table
        self.ball = ball

    def vs_table(self):
        """Check for collisions between ball and table. Adjust ball velocity accordingly and reverse the movement of the ball."""
        # Als de bal short cushion raakt
        if -self.table.get_short_cushion() > self.ball.get_position().z - self.ball.get_radius() or self.ball.get_position().z + self.ball.get_radius() > self.table.get_short_cushion():
            self.ball.update(direction=-1)
            self.ball.invert_z_velocity()
        # Als de ball long cushion raakt
        if self.ball.get_position().x + self.ball.get_radius() > self.table.get_long_cushion() or -self.table.get_long_cushion() > self.ball.get_position().x - self.ball.get_radius():  
            self.ball.update(direction=-1)
            self.ball.invert_x_velocity()

    def vs_balls(self, balls):
        """Check for collisions between ball and all the balls. Adjust the velocity of both balls in the collisions and reverse the movement of the ball."""
        for ball in balls:
            if ball == self.ball:
                continue
            distance = 2.0 * self.ball.get_radius()  # afstand om botsingen te controleren
            # diff = de vector tussen de twee bollen
            diff = ball.get_position() - self.ball.get_position()  # vector tussen de twee
            if mag(diff) < distance:
                # vector loodrecht op de vector diff
                dtan = rotate(diff, radians(90), vector(0, 1, 0))
                # neem de twee snelheden
                velocity_ball = ball.get_velocity()
                velocity_self_ball = self.ball.get_velocity()
                # draai de laatste tijdstap terug
                ball.update(direction=-1)
                self.ball.update(direction=-1)
                # haal de lood- en raaklijnen op
                velocity_ball_rad = proj(velocity_ball, diff)
                velocity_ball_tan = proj(velocity_ball, dtan)
                velocity_self_ball_rad = proj(velocity_self_ball, -diff)
                velocity_self_ball_tan = proj(velocity_self_ball, dtan)
                # draai de loodlijnen om en bewaar de raaklijnen
                ball.set_velocity(velocity_self_ball_rad + velocity_ball_tan)
                self.ball.set_velocity(velocity_ball_rad + velocity_self_ball_tan)

# snelheden: 35 km/h => 10 m/s => 10000 mm / s => 30000 mm / (1/30 s)


if __name__ == '__main__':
    # hoofdstuk 6 cs python
    scene.background = 0.8 * vector(1, 1, 1)  # Lichtgrijs (0.8 van 1.0)
    scene.width = 1680                         # Maak het 3D-scherm groter
    scene.height = 1280

    RATE=30
    dT = 1.0/RATE

    table = Table(table_typen["Biljart"]["match"]["height"], table_typen["Biljart"]["match"]["width"], table_typen["Biljart"]["match"]["cushion"])
    location_1 = vector(-table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], table_typen["Biljart"]["match"]["acquit"])
    location_2 = vector(-table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], 0)
    location_3 = vector(table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], 0)
    locations = [location_1, location_2, location_3]
    balls = [Ball(ballen_typen["Biljart"]["size"], vector(.8, .8, .8), loc, dT) for loc in locations]


    while True:
        rate(RATE)
        for ball in balls:
            ball.update()
            c_detector = Collision(table, ball)
            c_detector.vs_table()
            c_detector.vs_balls(balls)


        

