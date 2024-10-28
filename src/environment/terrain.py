import random

class Terrain:
    # speed multiplier
    types = {"sand": 0.7, "snow": 0.8, "asphalt": 1}

    def __init__(self, terrain):
        self.terrain = terrain
        self.speed_mult = self.types[terrain]

    @classmethod
    def random_terrain(cls):
        # return random terrain type
        terrain = random.choice(list(cls.types.keys()))
        return cls(terrain)

    def get_mult(self):
        return self.speed_mult

segments = [Terrain.random_terrain().get_mult() for i in range(5)]
print(segments)
