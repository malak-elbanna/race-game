from src.environment.car import Car
from src.environment.track import Track
from src.environment.obs_reward import Obstacles, Rewards

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

    def simple_reward(self):
        if self.car.position >= self.track.length:
            return 100  
        elif self.car.battery <= 0 or self.car.speed == 0:
            return -100

        segment = self.track.get_segment(self.car.position)
        if isinstance(segment, Obstacles):
            return -20
        if isinstance(segment, Rewards):
            return 30
        
        return -1

    def reward_function(self):
        if self.car.position >= self.track.length:
            return 100  
        elif self.car.battery <= 0 or self.car.speed == 0:
            return -100  

        segment = self.track.get_segment(self.car.position)
        reward = 0

        if isinstance(segment, Obstacles):
            if segment.type == "wall":
                if self.car.speed > 2:
                    reward += -10  
                else: 
                    reward += -30
            elif segment.type == "animal":
                reward += -15
            elif segment.type == "mud":
                reward += -5

        if isinstance(segment, Rewards):
            if segment.type == "small_coin":
                reward += 5
            elif segment.type == "big_coin":
                reward += 50
            elif segment.type == "benzene":
                if self.car.battery < 50:
                    reward += 20 
                else:
                    reward += 10
            elif segment.type == "speed_boost":
                if self.car.speed <= 2:
                    reward += 10 
                else:
                    reward += 5
            elif segment.type == "nitro_boost":
                if self.car.speed <= 2:
                    reward += 20 
                else: 
                    reward += 10

        steps_to_goal = (self.track.length - self.car.position) / max(self.car.speed, 0.1)
        battery_consumption = steps_to_goal * 0.2 * self.car.speed

        if battery_consumption > self.car.battery:
            reward -= (self.track.length - self.car.position) + 100

        speed_penalty = (self.car.MAX_SPEED - self.car.speed) * 0.3
        battery_penalty = (100 - self.car.battery) * 0.5
        progress_reward = (self.car.position / self.track.length) * 10  

        return reward + progress_reward - (speed_penalty + battery_penalty)

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
    
    def get_state(self):
        return (self.car.position, self.car.speed, self.car.battery, self.car.coins)
