from track import Track

class Car:
    def __init__(self, track_length):
        self.position = 0
        self.speed = 1
        self.battery = 100
        self.track = Track(track_length)

    def accelerate(self):
        pass
    
    def decelerate(self):
        pass

    def recharge(self):
        pass

    def move(self):
        # transition function
        # changes speed, position, battery according to segment info
        pass