from track import Track

class Car:
    def __init__(self, track_length):
        self.position = 0
        self.speed = 1
        self.battery = 100
        self.track = Track(track_length)
        self.coins = 0

    def accelerate(self):
        self.speed += 1
    
    def decelerate(self):
        if self.speed <= 1:
            self.speed = 1
        else:
            self.speed -= 1

    def recharge(self):
        if 70 < self.battery < 100:
            self.battery += 20
    def collect_coin(self,amount):
        self.coins += amount

    def move(self):
        # transition function
        # changes speed, position, battery according to segment info
        seg_info = self.track.get_segment(self.position)
        
        terrain = seg_info["terrain"]
        self.speed *= terrain.get_mult()
        self.battery -= (self.speed * 0.3)

        self.position += int(self.speed)
