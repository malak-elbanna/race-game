from track import Track
from terrain import Terrain
from obs_reward import Obstacles, Rewards

class Car:
    MAX_BATTERY = 100
    MAX_SPEED = 5

    def __init__(self, track_length):
        self.position = 0
        self.speed = 1
        self.battery = 100
        self.track = Track(track_length)
        self.coins = 0

    def accelerate(self):
        self.speed = min(self.speed + 1, self.MAX_SPEED)
    
    def decelerate(self):
        self.speed = max(self.speed - 1, 1)

    def recharge(self):
        if self.battery <= 70:  
            self.battery = min(self.battery + 20, self.MAX_BATTERY)
            return True
        return False

    def collect_coin(self, amount):
        self.coins += amount

    def move(self):
        self.battery -= (self.speed * 0.2)
        self.battery = max(0, self.battery)

        seg_info = self.track.get_segment(self.position)

        if isinstance(seg_info, Terrain):
            original = self.speed
            self.speed = max(1, min(original * seg_info.get_mult(), self.MAX_SPEED))

        elif isinstance(seg_info, Obstacles):
            seg_info.impact(self)

        elif isinstance(seg_info, Rewards):
            seg_info.impact(self)

        self.position += max(1, int(self.speed))