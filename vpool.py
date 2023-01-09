
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
        bound_b = box(pos=vector(-(self.height + 4.75 * self.cushion)//2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.color_wood)
        bound_c = box(pos=vector(0, self.cushion // 2, (self.width + 4.75 * self.cushion) //2), axis=vector(1, 0, 0), size=vector(self.height + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.color_wood)  
        bound_d = box(pos=vector((self.height + 4.75 * self.cushion) //2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 7.75 * self.cushion, 1.2 * self.cushion, 3 * self.cushion), color=self.color_wood)   

        objects = [wall_a, wall_b, wall_c, wall_d, bound_a, bound_b, bound_c, bound_d]
        # return compound(objects, pos=vector(0,0,0))

    def invalid_position(self, ball):
        # Als de bal wall_a raakt
        if (-(self.width - self.cushion) // 2) > ball.get_position().z - ball.get_radius():  # Geraakt -- vergelijk de x-positie
            ball.invert_z_velocity()
            return
        if ball.get_position().z + ball.get_radius() > (self.width - self.cushion) // 2:  # Geraakt -- vergelijk de x-positie
            ball.invert_z_velocity()
            return
        # Als de ball wall_b raakt
        if ball.get_position().x + ball.get_radius() > (self.height - self.cushion) // 2:  # Geraakt -- vergelijk de z-positie
            ball.invert_x_velocity()
            return
        if (-(self.height - self.cushion) // 2) > ball.get_position().x - ball.get_radius():  # Geraakt -- vergelijk de z-positie
            ball.invert_x_velocity()
            return


class Ball:

    def __init__(self, radius, color, location, dt) -> None:
        self.dt = dt
        self.radius = radius
        self.ball = sphere(radius=radius, pos=location, color=color)
        self.ball.vel = vector(-3000, 0, 3000)

    def update(self, direction=1):
        self.ball.pos = self.ball.pos + self.ball.vel * self.dt * direction

    def get_position(self):
        return self.ball.pos

    def get_radius(self):
        return self.radius

    def invert_z_velocity(self):
        self.ball.vel.z *= -1.0

    def invert_x_velocity(self):
        self.ball.vel.x *= -1.0



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
            table.invalid_position(ball)


        

