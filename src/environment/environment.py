from car import Car
from track import Track

class Environment:
    def __init__(self, track_length):
        self.track = Track(track_length)
        self.car = Car(track_length)
        self.rebuild()
    
    def rebuild(self):
        self.car.position = 0
        self.car.battery = 100
        self.car.speed = 1
        self.track.init_track()
    
    def step(self, action):
        # make the action and change env
        # will be used in search
        pass

    def game_over(self):
        # check if car finished track
        pass