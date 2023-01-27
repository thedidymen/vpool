from vpython import *

import logging
import logging.config


# Sizes in tenths of milimeters
table_typen = {
    "Biljart": {
        "match": {
            "height": 28400,
            "width": 14200,
            "acquit": 1825,
            "cushion": 370,
        },
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

colors = [
    {"color": "WHITE", "vector": vector(255/255, 255/255, 255/255)},  
    {"color": "YELLOW", "vector": vector(255/255, 255/255, 0)},
    {"color": "RED", "vector": vector(255/255, 0, 0)},
]

# Sizes in tenths of milimeters
ballen_typen = {
    "Biljart": {
        "size": 615 // 2
    },
}

class Color:

    def __init__(self, color, vec):
        self.color = color
        self.vec = vec

    def __repr__(self):
        return self.color

    def rgb(self):
        return self.vec


class Table:

    GREEN = vector(118/255,238/255, 0)
    WOOD = vector(133/255, 94/255, 66/255)

    def __init__(self, height, width, cushion, holes=False):
        self.cushion = cushion
        self.height = height
        self.width = width
        self.holes = holes
        self.table = self.create_table()

    def __repr__(self):
        return "Table"

    def create_table(self):
        ground = box(size=vector(self.height + self.cushion, 1, self.width + self.cushion), pos=vector(0, -1, 0), color=self.GREEN)
        
        wall_a = box(pos=vector(0, self.cushion // 2, -(self.width + self.cushion) // 2), axis=vector(1, 0, 0), size=vector(self.height + 1.65 * self.cushion, self.cushion, self.cushion), color=self.GREEN)
        wall_b = box(pos=vector(-(self.height + self.cushion) // 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 1.65 * self.cushion, self.cushion, self.cushion), color=self.GREEN)
        wall_c = box(pos=vector(0, self.cushion // 2, (self.width + self.cushion) // 2), axis=vector(1, 0, 0), size=vector(self.height + 1.65 * self.cushion, self.cushion, self.cushion), color=self.GREEN)  
        wall_d = box(pos=vector((self.height + self.cushion) // 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 1.65 * self.cushion, self.cushion, self.cushion), color=self.GREEN)   
        
        wall_a.rotate(angle=pi/11.)
        wall_b.rotate(angle=-pi/11.)
        wall_c.rotate(angle=-pi/11.)
        wall_d.rotate(angle=pi/11.)

        bound_a = box(pos=vector(0, self.cushion // 2, -(self.width + 4.75 * self.cushion) // 2), axis=vector(1, 0, 0), size=vector(self.height + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.WOOD)
        bound_b = box(pos=vector(-(self.height + 4.75 * self.cushion)// 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.WOOD)
        bound_c = box(pos=vector(0, self.cushion // 2, (self.width + 4.75 * self.cushion) //2), axis=vector(1, 0, 0), size=vector(self.height + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.WOOD)  
        bound_d = box(pos=vector((self.height + 4.75 * self.cushion) // 2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.WOOD)   

        objects = [wall_a, wall_b, wall_c, wall_d, bound_a, bound_b, bound_c, bound_d]
        # return compound(objects, pos=vector(0,0,0))

    def get_short_cushion(self):
        """Return location of short cushion."""
        return (self.width - 0.5 * self.cushion) // 2

    def get_long_cushion(self):
        """Return location of long cushion."""
        return (self.height - 0.5 * self.cushion) // 2


class Ball:

    def __init__(self, radius, color, location, dt):
        """Create a ball with a radius (int), color (Color) and location (vector). dT (float) is the time interval for each update."""
        self.dt = dt
        self.radius = radius
        self.ball = sphere(radius=radius, pos=location, color=color.rgb())
        self.ball.vel = vector(0, 0, 0)
        self.collisions = []
        self.color = color

    def __repr__(self):
        return str(self.color)

    def update(self, direction=1):
        """Move the ball, apply friction."""
        self.move(direction)
        self.friction()

    def friction(self):
        """Progressively apply friction and set velocity to zero when the magnitude approached zero."""
        magnitude = self.get_velocity().mag
        friction = 1.0
        if magnitude > 3000:            # progressive increase in friction to prevent long waiting for the balls to stop 
            friction = 0.996
        elif magnitude > 1000:
            friction = 0.96
        elif magnitude > 300:
            friction = 0.85
        elif magnitude > 10:
            friction = 0.6
        else:
            self.ball.vel = vector(0, 0, 0)

        self.ball.vel *= friction       # some how getting fancy with setter en getter breaks this code! If it ain't broke, dont fix it!
    
    def move(self, direction):
        """Update ball position with its velocity multiplied by delta T for directions times. Negative directions reverses steps."""
        self.set_position(self.get_position() + self.get_velocity() * self.dt * direction)

    def get_position(self):
        """Get ball position, returns vector."""
        return self.ball.pos

    def set_position(self, pos):
        """Get ball position, returns vector."""
        self.ball.pos = pos

    def get_velocity(self):
        """Get ball velocity, returns vector."""
        return self.ball.vel

    def set_velocity(self, vel):
        """Set ball velocity, takes vector."""
        self.ball.vel = vel

    def get_radius(self):
        """Get ball radius, returns int."""
        return self.radius

    def invert_z_velocity(self):
        """Invert the z component of the velocity."""
        self.ball.vel.z *= -1.0

    def invert_x_velocity(self):
        """Invert the x component of the velocity."""
        self.ball.vel.x *= -1.0

    def has_speed(self):
        """Returns True if ball still has speed."""
        return self.get_velocity().mag > 0

    def collision(self, other):
        """Appends other to collision list."""
        self.collisions.append(other)

    def get_collisions(self):
        """Returns collision list."""
        return self.collisions

    def reset_collisions(self):
        """Resets collision list."""
        self.collisions = []


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
            self.ball.collision("CUSHION")
        # Als de ball long cushion raakt
        if self.ball.get_position().x + self.ball.get_radius() > self.table.get_long_cushion() or -self.table.get_long_cushion() > self.ball.get_position().x - self.ball.get_radius():  
            self.ball.update(direction=-1)
            self.ball.invert_x_velocity()
            self.ball.collision("CUSHION")

    def vs_balls(self, balls):
        """Check for collisions between ball and all the balls. Adjust the velocity of both balls in the collisions and reverse the movement of the ball."""
        for ball in balls:

            if ball == self.ball:
                continue

            distance = 2.0 * self.ball.get_radius()  # afstand om botsingen te controleren
            # diff = de vector tussen de twee bollen

            diff = ball.get_position() - self.ball.get_position()  # vector tussen de twee
            if mag(diff) < distance:

                # register collision with both balls
                # TO DO: these two lines seem to increase the likelyhood of a clipping ball
                self.ball.collision(str(ball))
                ball.collision(str(self.ball))

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

    def __init__(self, power=5000, max_power=20000):
        """Generate object to show direction and speed of cue-ball."""
        self.rod = cylinder(pos = vector(0, 50, 0), axis = vector(1000, 0, 0),radius = 20, color = vector(139, 69, 19)/255)
        self.angle = 0
        self.power = power
        self.max_power = max_power

    def change_angle(self, direction, change=1):
        """Change current angle for applying force to cue-ball, takes direction (-1 or 1) and change in degrees (default = 1)."""
        if direction not in [-1, 1]:
            raise ValueError
        self.angle = self.angle + direction * change
        self.angle %= 360
    
    def get_angle(self):
        """Get current angle of cue-ball."""
        return self.angle

    def change_power(self, direction, change=100):
        """Change power of next shot, takes direction (-1 or 1) and change (cast to int)."""
        self.power = int(self.power + direction * change) 
        self.power = min(self.power, self.max_power)
        self.power = max(self.power, 0)

    def get_power(self):
        """Get current power of cue-ball."""
        return self.power

    def new_velocity(self):
        """Calculate the new velocity for the next shot."""
        rad = radians(cue.get_angle())
        return vector(cue.get_power() * cos(rad), 0, cue.get_power() * sin(rad))

    def visible(self):
        """Turn cue visible."""
        self.rod.opacity = 1

    def invisible(self):
        """Turn cue invisible."""
        self.rod.opacity = 0


class Score:

    def hit_objects(self, objects, collisions):
        """Return Bool if all objects are hit."""
        set_collisions = set(collisions)
        # logger.debug("set:", set_collisions, "any:", [object in set_collisions for object in objects])
        return all([object in set_collisions for object in objects])

    def cushion_first(self, collisions):
        """Returns bool if cushion was hit first"""
        return collisions[0] == "CUSHION"

    def n_cushions(self, objects, collisions, n):
        """Returns bool if n cushions are hit before hitting last object in objects"""
        if self.hit_objects(objects, collisions):
            index = max(idx for idx, val in enumerate(collisions) if val in objects)
            return collisions[:index].count("CUSHION") >= n
        return False

class LibreScore(Score):

    def __init__(self, players, objects, points, turns=20):
        super().__init__()
        self.players = players
        self.score = {player: 0 for player in players}
        self.turns = turns
        self.turn = 1
        self.objects = [objects]
        self.points = points

    def __repr__(self):
        s = ""
        for player in self.players:
            s += f"{player}: {self.score[player]}, "
        s += f"turn: {self.turn}"
        return s

    def next_turn(self):
        self.turn += 1

    def get_turn(self):
        return self.turn

    def get_player_score(self, player):
        return self.score[player]

    def score_shot(self, player, collisions):
        for object in self.objects:
            if self.hit_objects(object, collisions):
                self.score[player] = self.score[player] + self.points




def keydown_func(evt):
    """This function is called each time a key is pressed."""
    key = evt.key

    # define keys to change power (w and s), angle (a, q and d, e)
    if key in 'w':
        cue.change_power(1)              # increase power
    elif key in 'W':
        cue.change_power(1, 1000)        # big increase power
    elif key in 's':
        cue.change_power(-1)             # decrease power
    elif key in 'S':
        cue.change_power(-1, 1000)       # big decrease power

    elif  key in 'a':
        cue.change_angle(-1)             # change angle counterclockwise
    elif  key in 'A':
        cue.change_angle(-1, 0.1)        # small change angle counterclockwise
    elif  key in 'q':
        cue.change_angle(-1, 10)         # big change angle counterclockwise
    elif  key in 'Q':
        cue.change_angle(-1, 90)         # huge change angle counterclockwise

    elif key in 'd':
        cue.change_angle(1)             # change angle clockwise
    elif key in 'D':
        cue.change_angle(1, 0.1)        # small change angle clockwise
    elif key in 'e':
        cue.change_angle(1, 10)         # big change angle clockwise
    elif key in 'E':
        cue.change_angle(1, 90)         # huge change angle clockwise

    elif key in ' ':                    # shoot cue-ball in given direction
        balls[0].set_velocity(cue.new_velocity())
        
    elif key in 'z':                    # sets velocity of cueball to zero
        balls[0].set_velocity(vector(0, 0, 0))
    elif key in 'x':                    # sets velocity of all balls to zero
        for ball in balls:
            ball.set_velocity(vector(0, 0, 0))


# def click_fun(event):
#     """This function is called each time the mouse is clicked."""
#     print("event is", event.event, event.which)

class Game:

    def __init__(self, table, balls, cue, score):
        self.table = table
        self.balls = balls
        self.cue = cue
        self.score = score

    def game_loop(self):
        while True:
            rate(RATE)
            self.balls_update()

    def balls_update(self):
        speed_vector = []
        for ball in self.balls:
            # move ball to next position
            ball.update()
            speed_vector.append(ball.has_speed())

            # check for collisions with objects
            c_detector = Collision(self.table, ball)
            c_detector.vs_table()
            c_detector.vs_balls(balls)

            # draw direction vector at current position
            self.cue.rod.axis = self.cue.new_velocity()
            self.cue.rod.pos = self.balls[0].get_position()

            # draw direction vector at current position
            if any(speed_vector):
                self.cue.invisible()
            else:
                for ball in self.balls:
                    if len(ball.get_collisions()) > 0:
                        self.score.score_shot("Reijer", ball.get_collisions())
                        scene.caption = f"""{score}"""
                        ball.reset_collisions()
                self.cue.visible()


if __name__ == '__main__':
    # notes:
    # snelheden: 35 km/h => 10 m/s => 10000 mm / s => 30000 mm / (1/30 s)

    # Set up logging
    # logger = logging.getLogger(__name__)
    # logging.config.fileConfig('logging.ini')
    # logger.warning("Setting up Vpool")

    # setting up canvas
    scene.background = 0.8 * vector(1, 1, 1)  # Lichtgrijs (0.8 van 1.0)
    scene.width = 1280                         # Maak het 3D-scherm groter
    scene.height = 720
    scene.bind('keydown', keydown_func)        # Functie voor toetsaanslagen
    # scene.bind('click', click_fun)            # Functie voor muiskliks
    scene.caption = """Hello World!"""

    # Constants
    RATE=30
    dT = 1.0/RATE

    # create table object
    table = Table(table_typen["Biljart"]["match"]["height"], table_typen["Biljart"]["match"]["width"], table_typen["Biljart"]["match"]["cushion"])
    
    # create staring positions for balls
    # TO DO: move to class for starting positions for libre
    location_1 = (vector(-table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], table_typen["Biljart"]["match"]["acquit"]), Color(colors[0]["color"], colors[0]["vector"]))
    location_2 = (vector(-table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], 0), Color(colors[1]["color"], colors[1]["vector"]))
    location_3 = (vector(table_typen["Biljart"]["match"]["height"]//4, ballen_typen["Biljart"]["size"], 0), Color(colors[2]["color"], colors[2]["vector"]))
    locations = [location_1, location_2, location_3]

    # create balls for libre
    balls = [Ball(ballen_typen["Biljart"]["size"], loc[1], loc[0], dT) for loc in locations]
    cue = Cue()

    # fix camera position, currently based on magic numbers!
    scene.camera.pos = vector(-22000, 6500, 0)
    scene.camera.axis = vector(22000, -6500, 0)
    
    score = LibreScore(["Reijer"], ["YELLOW", "RED"], 1)

    game = Game(table, balls, cue, score)
    game.game_loop()
