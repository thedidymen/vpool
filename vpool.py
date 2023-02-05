from random import choice
from vpython import *


class Prog:

    def __init__(self, rate, settings, games_settings, players, easy_mode=False):
        """Create Program objects and settings"""
        self.easy_mode = easy_mode
        self.object_score = None

        self.menu_bool = True
        self.game_bool = False

        self.rate = rate
        self.settings = settings
        self.games_settings = games_settings
        self.players = players

        self.table = Table(settings["table"]["height"], settings["table"]["width"], settings["table"]["cushion"])
        self.caption = Caption()
        self.camera = Camera()

        # setting up table for menu animation.
        set_up_choice = choice([self.games_settings['Libre'], self.games_settings['Hundred'], self.games_settings['Over red']])
        self.game = Game(self.rate, self.settings["ball_size"], self.table, self.caption, set_up_choice, self.players, self.object_score)
        self.game.cue.invisible()


    def prog_loop(self):
        """The program loop."""
        while True:
            rate(self.rate)
            if self.menu_bool:
                self.menu_loop()
                
            if self.game_bool:
                self.game.game_loop()

            if self.game.game_state.finished:
                self.game.cue.invisible()
                self.caption.set_menu_and_score(self.game.score.victor())
                self.menu_bool, self.game_bool = self.game_bool, self.menu_bool
                self.game.game_state.finished = False


    def menu_loop(self):
        """Do menu animation."""
        self.camera.new_pos()

    def setup_game(self):
        """General setup for a game"""
        # reposition camera
        self.camera.set_game_play()
        # Clear previous game of objects and set up new game
        self.game.empty()
        # Go into game modus
        self.menu_bool, self.game_bool = self.game_bool, self.menu_bool

    def set_up_libre(self):
        """set caption and game specific settings for Libre"""
        self.setup_game()
        self.caption.set_libre()
        if self.easy_mode:
            self.object_score = 3
        self.game = Game(self.rate, self.settings["ball_size"], self.table, self.caption, self.games_settings['Libre'], self.players, self.object_score)

    def set_up_three_cushion(self):
        """set caption and game specific settings for Libre"""
        self.setup_game()
        self.caption.set_three_cushion()
        if self.easy_mode:
            self.object_score = 3
        self.game = Game(self.rate, self.settings["ball_size"], self.table, self.caption, self.games_settings['Three cushion'], self.players, self.object_score)

    def set_up_hundred(self):
        """set caption and game specific settings for Hundred"""
        self.setup_game()
        self.caption.set_hundred()
        if self.easy_mode:
            self.object_score = 5
        self.game = Game(self.rate, self.settings["ball_size"], self.table, self.caption, self.games_settings['Hundred'], self.players, self.object_score)

    def set_up_over_red(self):
        """set caption and game specific settings for Hundred"""
        self.setup_game()
        self.caption.set_over_red()
        if self.easy_mode:
            self.object_score = 2
        self.game = Game(self.rate, self.settings["ball_size"], self.table, self.caption, self.games_settings['Over red'], self.players, self.object_score)


class Game:

    def __init__(self, rate, ball_radius, table, caption, settings, players_list, object_score):
        """Setup a Game"""
        self.cue = Cue()
        self.game_state = GameState()
        self.radius = ball_radius
        self.dT = 1.0/rate
        self.table = table
        self.caption = caption

        # Setting up players
        self.players = players_list
        self.score = settings["score"](self.players, object_score)

        # create balls, setup cueballs and objectives
        self.balls = self.create_balls(settings)
        self.cueballs = [self.balls[idx] for idx in range(len(self.balls)) if settings["balls"]["cueballs"][idx]]
        self.objectives = [goal["Combinations"] for goal in settings["goals"]]

        # setup current player
        self.current_player = self.players[0]
        self.current_cueball = self.cueballs[0]
        self.current_objective = self.objectives[0]

    def create_balls(self, settings):
        """Sets up the ball required for the game."""
        locations = settings["balls"]["start_locations"]
        colors = settings["balls"]["colors"]
        return [Ball(self.radius, Color(colors[idx]["color"], colors[idx]["vector"]), location, self.dT) for idx, location in enumerate(locations)]

    def game_loop(self):
        """One iteration of the game loop."""
        self.place_cue()

        self.balls_update()
        self.game_state.moving_balls = self.moving_balls()

        if self.game_state.moving_balls:
            self.cue.invisible()
            self.game_state.shot = True
        
        if self.game_state.shot and not self.game_state.moving_balls:
            self.game_state.lose_turn = self.score_points()

            if not self.game_state.lose_turn:
                self.change_player()
                if self.game_finished():
                    self.game_state.finished = True
        
            self.setup_turn()

            self.game_state.shot = False
            self.game_state.lose_turn = False

        self.caption.update(self.current_player, self.score)

    def empty(self):
        """Previous game objects cannot be delete in VPython, set them to invisible."""
        for ball in self.balls:
            ball.invisible()

    def game_finished(self):
        """A base game never finishes."""
        return False

    def setup_turn(self):
        """Clears collisions registered by the balls, replaces the cue and makes it visible."""
        self.reset_collision_balls()
        self.place_cue()
        self.cue.visible()

    def balls_update(self):
        """Updates all the balls to the new positions and checks for collisions with the table and other balls."""
        for ball in self.balls:
            ball.update()                             # move ball to next position
            c_detector = Collision(self.table, ball)  # check for collisions with objects
            c_detector.vs_table()
            c_detector.vs_balls(self.balls)

    def score_points(self):
        """Score points if conditions are met."""
        lose_turn = False
        if len(self.current_cueball.get_collisions()) > 0:
            lose_turn = self.score.score_shot(self.current_player, self.current_objective, self.current_cueball.get_collisions())
        return lose_turn

    def change_player(self):
        """Change to next player."""
        self.next_turn()
        self.next_player()
        self.next_objective()
        self.next_cueball()

    def place_cue(self):
        """Reposition the cue"""
        self.cue.rod.axis = self.cue.new_velocity()
        self.cue.rod.pos = self.current_cueball.get_position()

    def reset_collision_balls(self):
        """Clear all registered collisions."""
        for ball in self.balls:
            ball.reset_collisions()

    def moving_balls(self):
        """Return bool if any ball has speed"""
        return any([ball.has_speed() for ball in self.balls])

    def next_object(self, current_object, objects):
        """Takes current_object (item in list) and objects (list), returns next object in list or loops to first item in the list."""
        current_object_index = objects.index(current_object)
        new_objective_index = (current_object_index + 1) % len(objects)
        return objects[new_objective_index]

    def next_player(self):
        """Determine next player."""
        self.current_player = self.next_object(self.current_player, self.players)

    def next_objective(self):
        """Determines next objective, for Libre the objective should alternate in an odd player game."""
        self.current_objective = self.next_object(self.current_objective, self.objectives)

    def next_cueball(self):
        """Determines next cueball."""
        self.current_cueball = self.next_object(self.current_cueball, self.cueballs)

    def next_turn(self):
        """After both player have taken a turn, increase turn maker."""
        if (self.players.index(self.current_player) + 1) // len(self.players):
            self.score.next_turn()

    def stop_balls(self):
        """Stops movement of all balls"""
        for ball in self.balls:
            ball.set_velocity(vector(0, 0, 0))

    def get_cueball(self):
        """Return current cueball"""
        return self.current_cueball

    def game_finished(self):
        return self.score.check_victor()


class GameState:

    def __init__(self):
        """Set up game states, to keep track of current state of the game."""
        # Turn states
        self.shot = False
        self.moving_balls = False
        self.lose_turn = False
        self.finished = False


class Table:

    GREEN = vector(118/255,238/255, 0)
    WOOD = vector(133/255, 94/255, 66/255)

    def __init__(self, height, width, cushion, holes=False):
        """Set up the playing table."""
        self.cushion = cushion
        self.height = height
        self.width = width
        self.holes = holes
        self.table = self.create_table()

    def __repr__(self):
        """Set respresentation of instance of Table"""
        return "Table"

    def create_table(self):
        """Create model of the table."""
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
        """Set respresentation of instance of Ball"""
        return str(self.color)

    def update(self, direction=1):
        """Move the ball, apply friction."""
        self.move(direction)
        self.friction()

    def friction(self):
        """Progressively apply friction and set velocity to zero when the magnitude approached zero."""
        magnitude = self.get_velocity().mag
        friction = 1.0
        if magnitude > 10000:            # progressive increase in friction to prevent long waiting for the balls to stop 
            friction = 0.999
        elif magnitude > 3000:
            friction = 0.995
        elif magnitude > 1000:
            friction = 0.99
        elif magnitude > 500:
            friction = 0.85
        elif magnitude > 100:
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

    def invisible(self):
        """Turn ball invisible"""
        self.ball.visible = False


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

            distance = 2.0 * self.ball.get_radius()  # Distance between point representation of balls

            diff = ball.get_position() - self.ball.get_position()  # vector tussen de twee
            if mag(diff) < distance:

                # register collision with both balls
                # TO DO: these two lines seem to increase the likelyhood of a clipping ball
                self.ball.collision(str(ball))
                ball.collision(str(self.ball))

                # Vector perpendicular to vector diff
                dtan = rotate(diff, radians(90), vector(0, 1, 0))

                # neem de twee snelheden
                velocity_ball = ball.get_velocity()
                velocity_self_ball = self.ball.get_velocity()

                # Turn back time one step
                ball.update(direction=-1)
                self.ball.update(direction=-1)

                # get perpendicular and tangent line
                velocity_ball_rad = proj(velocity_ball, diff)
                velocity_ball_tan = proj(velocity_ball, dtan)
                velocity_self_ball_rad = proj(velocity_self_ball, -diff)
                velocity_self_ball_tan = proj(velocity_self_ball, dtan)

                # rotate perpendicular lines and keep tangent lines
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
        rad = radians(self.get_angle())
        return vector(self.get_power() * cos(rad), 0, self.get_power() * sin(rad))

    def visible(self):
        """Turn cue visible."""
        self.rod.opacity = 1

    def invisible(self):
        """Turn cue invisible."""
        self.rod.opacity = 0


class Camera:

    def __init__(self):
        """"""
        self.angle = 0
        self.distance = 22000
        scene.camera.pos = vector(-23000, 6500, -0)
        scene.camera.axis = vector(23000, -6500, 0)

    def new_pos(self):
        """Calculate the new velocity for the next shot."""
        self.angle += .5
        self.angle %= 360
        rad = radians(self.angle)
        scene.camera.pos = vector(-self.distance * cos(rad), 6500, -self.distance * sin(rad))
        scene.camera.axis = vector(self.distance * cos(rad), -6500, self.distance * sin(rad))

    def set_game_play(self):
        """Set camera to game play start position"""
        scene.camera.pos = vector(-23000, 6500, 0)
        scene.camera.axis = vector(23000, -6500, 0)

    def move_x(self, direction, change=1000):
        """Move camera over x axis"""
        scene.camera.pos = vector(scene.camera.pos.x - direction * change, scene.camera.pos.y, scene.camera.pos.z)
        scene.camera.axis = vector(scene.camera.axis.x - direction * change, scene.camera.axis.y, scene.camera.axis.z)

    def move_z(self, direction, change=1000):
        """Move camera over z axis"""
        scene.camera.pos = vector(scene.camera.pos.x, scene.camera.pos.y, scene.camera.pos.z - direction * change)
        scene.camera.axis = vector(scene.camera.axis.x, scene.camera.axis.y, scene.camera.axis.z - direction * change)


class Color:

    def __init__(self, color, vec):
        """Connect colorname to color vector"""
        self.color = color
        self.vec = vec

    def __repr__(self):
        """Set respresentation of instance of Color"""
        return self.color

    def rgb(self):
        """Return the color-vector"""
        return self.vec


class Score:

    def hit_objective(self, objects, collisions):
        """Return Bool if all objectives are hit."""
        set_collisions = set(collisions)
        return all([object in set_collisions for object in objects])

    def hit_objective_in_order(self, objects, collisions):
        """Return Bool if all objectives are hit."""
        ordered_set = list(dict.fromkeys(collisions))
        strip_cushions = [obj for obj in ordered_set if obj != 'CUSHION']
        return objects == strip_cushions

    def cushion_first(self, collisions):
        """Returns bool if cushion was hit first"""
        return collisions[0] == "CUSHION"

    def n_cushions(self, objective, collisions, n):
        """Returns bool if n cushions are hit before hitting last object in objectives"""
        if self.hit_objectives(objective, collisions):
            index = max(idx for idx, val in enumerate(collisions) if val in objective)
            return collisions[:index].count("CUSHION") >= n
        return False


class LibreScore(Score):

    def __init__(self, players, object_score):
        """Set up score for the Libre game."""
        super().__init__()
        self.players = players
        self.score = {player: 0 for player in players}
        self.turn = 1
        self.object_score = 20 if object_score == None else object_score

    def __repr__(self):
        """Set respresentation of instance of LibreScore"""
        s = "Current score: "
        for player in self.players:
            s += f"{player}: {self.score[player]}, "
        s += f"turn: {self.turn}"
        return s

    def victor(self):
        """Determine the winner"""
        s = str(self)
        victors = [key for key, value in self.score.items() if value == max(self.score.values())]
        if len(victors) > 1:
            return f"{s}\nWinnaars: {', '.join(victors)}\n"
        return f"{s}\nWinnaar: {victors[0]}\n"

    def next_turn(self):
        """Increase turn marker by 1."""
        self.turn += 1

    def get_turn(self):
        """Return number of turns taken."""
        return self.turn

    def get_player_score(self, player):
        """Return the score of a player"""
        return self.score[player]

    def score_shot(self, player, objectives, collisions):
        """Determine if a player scored points based on collisions."""
        for objective in objectives:
            if self.hit_objective(objective["Combination"], collisions):
                self.score[player] = self.score[player] + objective["Points"]
                return True
        return False

    def check_victor(self):
        """Check if there is a winner."""
        if self.get_turn() == self.object_score:
            return True
        return False

class ThreeCushionScore(LibreScore):

    def __init__(self, players, object_score):
        """Set up score for the Libre game."""
        super().__init__()
        self.players = players
        self.score = {player: 0 for player in players}
        self.turn = 1
        self.object_score = 20 if object_score == None else object_score

    def score_shot(self, player, objectives, collisions):
        """Determine if a player scored points based on collisions."""
        for objective in objectives:
            if self.n_cushions(objective["Combination"], collisions, 3):
                self.score[player] = self.score[player] + objective["Points"]
                return True
        return False


class HundredScore(LibreScore):

    def __init__(self, players, object_score):
        """Setup Score for Hundred game"""
        super().__init__(players, object_score)
        self.object_score = 100 if object_score == None else object_score

    def victor(self):
        """Determine the winner"""
        s = str(self)
        victors = [key for key, value in self.score.items() if value == self.object_score]
        if len(victors) > 1:
            return f"{s}\nWinnaars: {', '.join(victors)}\n"
        return f"{s}\nWinnaar: {victors[0]}\n"

    def score_shot(self, player, objectives, collisions):
        """Determine if a player scored points based on collisions."""
        for objective in objectives:
            if self.hit_objective(objective["Combination"], collisions):
                self.score[player] = self.score[player] + objective["Points"]
                if self.score[player] > self.object_score:
                    self.score[player] = self.score[player] % self.object_score
                return True
        return False

    def check_victor(self):
        """Check if there is a winner."""
        for player in self.players:
            if self.score[player] == self.object_score:
                return True
        return False

class OverRedScore(LibreScore):

    def __init__(self, players, object_score):
        """Setup Score for Hundred game"""
        super().__init__(players, object_score)
        self.object_score = 10 if object_score == None else object_score

    def victor(self):
        """Determine the winner"""
        s = str(self)
        victors = [key for key, value in self.score.items() if value == self.object_score]
        if len(victors) > 1:
            return f"{s}\nWinnaars: {', '.join(victors)}\n"
        return f"{s}\nWinnaar: {victors[0]}\n"

    def score_shot(self, player, objectives, collisions):
        """Determine if a player scored points based on collisions."""
        if self.hit_objective_in_order(objectives[0]["Combination"], collisions):
            self.score[player] = self.score[player] + objectives[0]["Points"]
            if self.score[player] == self.object_score:
                return False
            return True
        if not self.hit_objective_in_order(objectives[1]["Combination"], collisions):
            if self.score[player] < 7:
                self.score[player] = 0
        return False

    def check_victor(self):
        """Check if there is a winner."""
        for player in self.players:
            if self.score[player] == self.object_score:
                return True
        return False


class Caption:

    def __init__(self):
        """Setup up caption interface to provide proper guidance throughout the game"""
        self.interface = self.explain_menu()
        self.game = ""
        self.update()

    def update(self, current_player=None, score=None):
        """Update scene caption"""
        if current_player != None:
            current_player = f"\nCurrent player: {current_player}"
        else:
            current_player = f""

        if score == None:
            scene.caption = f"""{self.interface}"""
        else:
            scene.caption = f"""{score}{current_player}\n{self.game}{self.interface}"""

    def empty(self):
        """Clear caption."""
        scene.caption = ""

    def set_libre(self):
        """Select text for Libre game"""
        self.interface = self.explain_interface()
        self.game = self.explain_libre()

    def set_hundred(self):
        """Select text for Hundred game"""
        self.interface = self.explain_interface()
        self.game = self.explain_hundred()

    def set_over_red(self):
        """Select text for 10 over Red game"""
        self.interface = self.explain_interface()
        self.game = self.explain_over_red()

    def set_three_cushion(self):
        """Select text for Three Cushion game"""
        self.interface = self.explain_interface()
        self.game = self.explain_three_cushion()

    def set_menu(self):
        """Select text for menu"""
        self.interface = self.explain_menu()

    def set_menu_and_score(self, victor):
        """Select text for menu"""
        scene.caption = f"""{victor}{self.explain_menu()}"""

    def explain_libre(self):
        """Explanation for Libre"""
        return  """
Game rules:
Players take turns and try to hit the other two balls with their cueball. Making this carambool will result in a point. The player with the most points after 20
turns wil win the game. (Easy mode = 3 turns)
"""

    def explain_three_cushion(self):
        """Explanation for Three Cushion"""
        return  """
Game rules:
Players take turns and try to hit the other two balls with their cueball, however three cushions need to be hit before hitting the final ball. Making this carambool 
will result in a point. The player with the most points after 20 turns wil win the game. (Easy mode = 3 turns)
"""

    def explain_hundred(self):
        """Explanation for Hundred"""
        return  """
Game rules:
Players take turns and try to hit a ball combination with the cueball. Hitting all other balls gives 20 points, Blue and Yellow are 4 points. Any combination 
with Red is 1 point. The player with exactly 100 points wins. Going over 100 points will get a penalty of 100 points. (Easy mode = 5 points)
"""

    def explain_over_red(self):
        """Explanation for 10 over Red"""
        return  """
Game rules:
Players make points by hitting the red ball first and then the yellow ball. Players lose all their points if they miss the red ball if current score is less 
than 7. Game wil stop if a player hits 10 points, there will be an equalizing turn. (Easy mode = 2 points)
"""

    def explain_interface(self):
        """Explanation for usin the game."""
        return """
Interface explaination:
The 'cue' give the direction and power of the shot. The angle can be adjusted clockwise: 'D' - 0.1, 'd' - 1, 'e' - 10, 'E' - 90 degrees;
or counterclockwise: 'A' - 0.1, 'a' - 1, 'q' - 10, 'Q' - 90 degrees. The power of the shot can be adjusted by: 'w' for increase or 's' for 
decrease, 'W' and 'S' will do a 10 fold jump. To take a shot press 'space bar'. The cueball can be stopped by pressing 'z' or 'x' for all 
balls. Right click on the mouse + moving will move the camera. The arrows wil move the camera around. Movement is relative to the in game 
coordinate system, not to the viewpoint of the observer. 'p' will quit the game.
"""

    def explain_menu(self):
        """Explanation for menu"""
        return """
Please Choose a game:
1. Libre
2. Hondertje maken
3. 10-over-rood
4. 3-Banden
"""
        

def keydown_func(evt):
    """Maps key presses to functions."""
    map = {
            'left': {'bools': [prog.game_bool], 'func': prog.camera.move_z, 'args': (1,)},
            'right': {'bools': [prog.game_bool], 'func': prog.camera.move_z, 'args': (-1,)},
            'up': {'bools': [prog.game_bool], 'func': prog.camera.move_x, 'args': (-1,)},
            'down': {'bools': [prog.game_bool], 'func': prog.camera.move_x, 'args': (1,)},

            'w': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_power, 'args': (1,)},
            'W': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_power, 'args': (1, 1000)},
            's': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_power, 'args': (-1,)},
            'S': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_power, 'args': (-1, 1000)},

            'a': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (-1,)},
            'A': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (-1, 0.1)},
            'q': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (-1, 10)},
            'Q': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (-1, 90)},

            'd': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (1,)},
            'D': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (1, 0.1)},
            'e': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (1, 10)},
            'E': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.cue.change_angle, 'args': (1, 90)},

            ' ': {'bools': [prog.game_bool, not prog.game.game_state.moving_balls], 'func': prog.game.get_cueball().set_velocity, 'args': (prog.game.cue.new_velocity(),)},
            'z': {'bools': [prog.game_bool], 'func': prog.game.get_cueball().set_velocity, 'args': (vector(0, 0, 0),)},
            'x': {'bools': [prog.game_bool], 'func': prog.game.stop_balls, 'args': ()}, 

            '1': {'bools': [prog.menu_bool], 'func': prog.set_up_libre, 'args': ()},
            '2': {'bools': [prog.menu_bool], 'func': prog.set_up_hundred, 'args': ()},
            '3': {'bools': [prog.menu_bool], 'func': prog.set_up_over_red, 'args': ()},
            '4': {'bools': [prog.menu_bool], 'func': prog.set_up_three_cushion, 'args': ()},  

        }

    key = evt.key

    if key in map.keys():
        if all([bool for bool in map[key]['bools']]):
            map[key]['func'](*map[key]['args'])

settings = {
    "table": {
        "height": 28400,
        "width": 14200,
        "acquit": 1825,
        "cushion": 370,
    },
    "ball_size": 615 // 2,
}

libre = {
    "balls": {
        "cueballs": [True, True, False],
        "colors": [
            {"color": "WHITE", "vector": vector(255/255, 255/255, 255/255)},
            {"color": "YELLOW", "vector": vector(255/255, 255/255, 0)},
            {"color": "RED", "vector": vector(255/255, 0, 0)},
        ],
        "start_locations": [
            vector(-settings["table"]["height"] // 4, settings["ball_size"], settings["table"]["acquit"]),
            vector(-settings["table"]["height"] // 4, settings["ball_size"], 0),
            vector(settings["table"]["height"] // 4, settings["ball_size"], 0),
        ],
    },
    "goals": [
        {
            "Cueball": "WHITE", 
            "Combinations": [
                {
                    "Combination": ["YELLOW", "RED"], 
                    "Points": 1
                },
            ],
        },{
            "Cueball": "YELLOW", 
            "Combinations": [
                {
                    "Combination": ["WHITE", "RED"], 
                    "Points": 1
                },
            ],
        },
    ],
    "score": LibreScore
}

hundred = {
    "balls": {
        "cueballs": [True, False, False, False],
        "colors": [
            {"color": "WHITE", "vector": vector(255/255, 255/255, 255/255)},
            {"color": "YELLOW", "vector": vector(255/255, 255/255, 0)},
            {"color": "RED", "vector": vector(255/255, 0, 0)},
            {"color": "BLUE", "vector": vector(0, 0, 255/255)},
        ],
        "start_locations": [
            vector(-settings["table"]["height"] // 4, settings["ball_size"], settings["table"]["acquit"]),
            vector(-settings["table"]["height"] // 4, settings["ball_size"], 0),
            vector(settings["table"]["height"] // 4, settings["ball_size"], 0),
            vector(0, settings["ball_size"], 0),
        ],
    },
    "goals": [
        {
            "Cueball": "WHITE", 
            "Combinations": [
                {
                    "Combination": ["YELLOW", "RED", "BLUE"], 
                    "Points": 20
                },
                {
                    "Combination": ["BLUE", "YELLOW"], 
                    "Points": 4
                },
                {
                    "Combination": ["RED", "BLUE"], 
                    "Points": 1
                },
                {
                    "Combination": ["YELLOW", "RED"], 
                    "Points": 1
                },
            ],
        },
    ],
    "score":  HundredScore,
}

over_red = {
    "balls": {
        "cueballs": [True, False, False],
        "colors": [
            {"color": "WHITE", "vector": vector(255/255, 255/255, 255/255)},
            {"color": "YELLOW", "vector": vector(255/255, 255/255, 0)},
            {"color": "RED", "vector": vector(255/255, 0, 0)},
        ],
        "start_locations": [
            vector(-settings["table"]["height"] // 4, settings["ball_size"], 0),
            vector(0, settings["ball_size"], 0),
            vector(settings["table"]["height"] // 4, settings["ball_size"], 0),
        ],
    },
    "goals": [
        {
            "Cueball": "WHITE", 
            "Combinations": [
                {
                    "Combination": ["RED", "YELLOW"], 
                    "Points": 1
                },
                {
                    "Combination": ["RED"], 
                    "Points": 0
                },
            ],
        }
    ],
    "score": OverRedScore
}

three_cushion = {
    "balls": {
        "cueballs": [True, True, False],
        "colors": [
            {"color": "WHITE", "vector": vector(255/255, 255/255, 255/255)},
            {"color": "YELLOW", "vector": vector(255/255, 255/255, 0)},
            {"color": "RED", "vector": vector(255/255, 0, 0)},
        ],
        "start_locations": [
            vector(-settings["table"]["height"] // 4, settings["ball_size"], settings["table"]["acquit"]),
            vector(-settings["table"]["height"] // 4, settings["ball_size"], 0),
            vector(settings["table"]["height"] // 4, settings["ball_size"], 0),
        ],
    },
    "goals": [
        {
            "Cueball": "WHITE", 
            "Combinations": [
                {
                    "Combination": ["YELLOW", "RED"], 
                    "Points": 1
                },
            ],
        },{
            "Cueball": "YELLOW", 
            "Combinations": [
                {
                    "Combination": ["WHITE", "RED"], 
                    "Points": 1
                },
            ],
        },
    ],
    "score": ThreeCushionScore
}


if __name__ == '__main__':
    # setting up canvas
    scene.background = 0.8 * vector(1, 1, 1)  # Lichtgrijs (0.8 van 1.0)
    scene.width = 1280                         # Maak het 3D-scherm groter
    scene.height = 700
    scene.title = 'Welcome to VPool!'
    scene.bind('keydown', keydown_func)        # Functie voor toetsaanslagen

    # fix camera position, currently based on magic numbers!
    scene.camera.pos = vector(-23000, 6500, 0)
    scene.camera.axis = vector(23000, -6500, 0)

    # Constants
    RATE=60
    games_settings = {
        'Libre': libre,
        'Hundred': hundred,
        'Over red': over_red,
        'Three cushion': three_cushion,
    }

    players = ["Player 1", "Player 2"]
    easy_mode = True

    prog = Prog(RATE, settings, games_settings, players, easy_mode)

    # start Game
    prog.prog_loop()
