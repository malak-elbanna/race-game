from src.environment.car import Car
from src.environment.track import Track

class Environment:
    def __init__(self, track_length):
        self.track = Track(track_length)
        self.car = Car(track_length)
        self.rebuild()
    
    def rebuild(self):
        self.car.position = 0
        self.car.battery = 100
        self.car.speed = 1
        self.car.coins = 0
        self.track.init_track(self.track.length)
    
    def step(self, action):
        if action == 'accelerate':
            self.car.accelerate()
        elif action == 'decelerate':
            self.car.decelerate()
        elif action == 'recharge':
            self.car.recharge()
        
        self.car.move()

        if self.game_over():
            print("game overrrr")
            return True

    def game_over(self):
        print(f"\nPostiion: {self.car.position} \n Battery: {self.car.battery} \nSpeed: {self.car.speed} \n")
        return self.car.position >= self.track.length or self.car.battery <= 0  or self.car.speed == 0