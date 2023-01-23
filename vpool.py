from vpython import *
from math import sin, cos, radians

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
        # TO DO: figure out why to multiply by .5 to make the balls touch the cushion.
        return (self.width - 0.5 * self.cushion) // 2

    def get_long_cushion(self):
        """Return location of long cushion."""
        # TO DO: figure out why to multiply by .5 to make the balls touch the cushion.
        return (self.height - 0.5 * self.cushion) // 2


class Ball:

    def __init__(self, radius, color, location, dt) -> None:
        """Create a ball with a radius (int), color (vector) and location (vector). dT (float) is the time interval for each update."""
        self.dt = dt
        self.radius = radius
        self.ball = sphere(radius=radius, pos=location, color=color)
        self.ball.vel = vector(0, 0, 0)

    def update(self, direction=1):
        """Updat ball position with its velocity multiplied by delta T for directions times. Negative directions reverses steps."""
        self.ball.pos = self.ball.pos + self.ball.vel * self.dt * direction

    def get_position(self):
        """Get ball position, returns vector"""
        return self.ball.pos

    def get_velocity(self):
        """Get ball velocity, returns vector"""
        return self.ball.vel

    def set_velocity(self, vel):
        """Set ball velocity, takes vector"""
        self.ball.vel = vel

    def get_radius(self):
        """Get ball radius, returns int"""
        return self.radius

    def invert_z_velocity(self):
        """Invert the z component of the velocity"""
        self.ball.vel.z *= -1.0

    def invert_x_velocity(self):
        """Invert the x component of the velocity"""
        self.ball.vel.x *= -1.0


class Collision:

    def __init__(self, table, ball):
        """Detect collisions between table and ball or between ball and other balls."""
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


class Cue:

    def __init__(self, power=5000, max_power=10000):
        """Generate object to show direction and speed of cue-ball"""
        self.rod = cylinder(pos = vector(0, 50, 0), axis = vector(1000, 0, 0),radius = 20, color = vector(139, 69, 19)/255)
        self.angle = 0
        self.power = power
        self.max_power = max_power

    def change_angle(self, direction, change=1):
        """Change current angle for applying force to cue-ball, takes direction (-1 or 1) and change in degrees (default = 1)"""
        if direction not in [-1, 1]:
            raise ValueError
        self.angle = self.angle + direction * change
        self.angle %= 360
    
    def get_angle(self):
        """Get current angle of cue-ball"""
        return self.angle

    def change_power(self, direction, change=300):
        """Change power of next shot, takes direction (-1 or 1) and change (cast to int)"""
        self.power = int(self.power + direction * change) 
        self.power = min(self.power, self.max_power)
        self.power = max(self.power, 0)

    def get_power(self):
        """Get current power of cue-ball"""
        return self.power

    def new_velocity(self):
        rad = radians(cue.get_angle())
        return vector(cue.get_power() * cos(rad), 0, cue.get_power() * sin(rad))


def keydown_func(evt):
    """This function is called each time a key is pressed."""
    key = evt.key

    # define keys to change power (w and s), angle (a and d)
    if key in 'w':
        cue.change_power(1)             # increase power
    elif  key in 'a':
        cue.change_angle(-1)            # change angle counterclockwise
    elif  key in 'q':
        cue.change_angle(-1, 10)        # change angle counterclockwise
    elif key in 's':
        cue.change_power(-1)             # decrease power
    elif key in 'd':
        cue.change_angle(1)            # change angle clockwise
    elif key in 'e':
        cue.change_angle(1, 10)        # fast change angle clockwise
    elif key in ' ':                    # shoot cue-ball in given direction
        vel = vector(cue.get_power() * cos(radians(cue.get_angle())), 0, cue.get_power() * sin(radians(cue.get_angle())))
        balls[0].set_velocity(cue.new_velocity())
    elif key in 'z':                    # sets velocity of cueball to zero
        balls[0].set_velocity(vector(0, 0, 0))
    elif key in 'x':                    # sets velocity of all balls to zero
        for ball in balls:
            ball.set_velocity(vector(0, 0, 0))


# def click_fun(event):
#     """This function is called each time the mouse is clicked."""
#     print("event is", event.event, event.which)

if __name__ == '__main__':
    # notes:
    # snelheden: 35 km/h => 10 m/s => 10000 mm / s => 30000 mm / (1/30 s)

    # setting up canvas
    scene.background = 0.8 * vector(1, 1, 1)  # Lichtgrijs (0.8 van 1.0)
    scene.width = 1680                         # Maak het 3D-scherm groter
    scene.height = 1280
    scene.bind('keydown', keydown_func)        # Functie voor toetsaanslagen
    # scene.bind('click', click_fun)            # Functie voor muiskliks
    scene.caption = """Hello World!"""

    # Constants
    RATE=30
    dT = 1.0/RATE
    RED = vector(255/255, 0, 0)
    YELLOW = vector(255/255, 255/255, 0)
    WHITE = vector(255/255, 255/255, 255/255)

    # create table object
    table = Table(table_typen["Biljart"]["match"]["height"], table_typen["Biljart"]["match"]["width"], table_typen["Biljart"]["match"]["cushion"])
    
    # create staring positions for balls
    # TO DO: move to class for starting positions for libre
    location_1 = (vector(-table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], table_typen["Biljart"]["match"]["acquit"]), YELLOW)
    location_2 = (vector(-table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], 0), WHITE)
    location_3 = (vector(table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], 0), RED)
    locations = [location_2, location_1, location_3]

    # create balls for libre
    balls = [Ball(ballen_typen["Biljart"]["size"], loc[1], loc[0], dT) for loc in locations]
    cue = Cue()


    while True:
        rate(RATE)
        for ball in balls:
            # move ball to next position
            ball.update()

            # check for collisions with objects
            c_detector = Collision(table, ball)
            c_detector.vs_table()
            c_detector.vs_balls(balls)

            # draw direction vector at current position
            cue.rod.axis = cue.new_velocity()
            cue.rod.pos = balls[0].get_position()
