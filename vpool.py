
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

# Sizes in tenths of milimeters
ballen_typen = {
    "Biljart": {
        "size": 615
    },
    "Pool": {
        "size": 572
    },
    "Snooker": {
        "size": 524
    },
}

class Table:

    def __init__(self, height, width, cushion, holes=False) -> None:
        self.cushion = cushion
        self.height = height
        self.width = width
        self.holes = holes
        self.color = vector(118/255,238/255, 0)

        ground = box(size=vector(self.height, 1, self.width), pos=vector(0, -1, 0), color=self.color)
        
        wall_a = box(pos=vector(0, self.cushion // 2, -(self.width + self.cushion) // 2), axis=vector(1, 0, 0), size=vector(self.height + 2 * self.cushion, self.cushion, self.cushion), color=self.color)
        wall_b = box(pos=vector(-(self.height + self.cushion)//2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 2 * self.cushion, self.cushion, self.cushion), color=self.color)
        wall_c = box(pos=vector(0, self.cushion // 2, (self.width + self.cushion) //2), axis=vector(1, 0, 0), size=vector(self.height + 2 * self.cushion, self.cushion, self.cushion), color=self.color)  
        wall_d = box(pos=vector((self.height + self.cushion) //2, self.cushion // 2, 0), axis=vector(0, 0, 1), size=vector(self.width + 2 * self.cushion, self.cushion, self.cushion), color=self.color)   


if __name__ == '__main__':
    scene.background = 0.8 * vector(1, 1, 1)  # Lichtgrijs (0.8 van 1.0)
    scene.width = 1680                         # Maak het 3D-scherm groter
    scene.height = 1280
    table = Table(table_typen["Biljart"]["match"]["height"], table_typen["Biljart"]["match"]["width"], table_typen["Biljart"]["match"]["cushion"])


    while True:
        rate(30)
        

