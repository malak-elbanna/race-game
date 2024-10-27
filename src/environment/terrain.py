import random

class Terrain:
    # speed multiplier
    types = {"sand": 0.7, "snow": 0.8, "asphalt": 1}

    def __init__(self, terrain):
        self.terrain = terrain
        self.speed_mult = self.types[terrain]

    def random_terrain(self):
        # return random terrain type
        pass

