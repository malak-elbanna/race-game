import random

class Obstacles:
    obs = ["wall", "animal",'mud']

    def __init__(self, obstacle):
        self.type = obstacle

    @classmethod
    def random_obstacle(cls):
        # Randomly select an obstacle type
        obstacle = random.choice(cls.obs)
        return cls(obstacle)
    
    def impact(self, car):
        if self.type == "wall":
            car.speed = max(0, car.speed - 2)
        elif self.type == "animal":
            car.decelerate()
            car.battery -= 3
        elif self.type == "mud":
            car.speed = max(1, car.speed * 0.7)

class Rewards:
    rews = ["small_coin",'big_coin', "benzene",'speed_boost','nitro_boost']

    def __init__(self, reward):
        self.type = reward
    
    @classmethod
    def random_reward(cls):
        # Randomly select a reward type
        reward = random.choice(cls.rews)
        return cls(reward)

    def impact(self,car):
        if self.type == "small_coin":
            car.collect_coin(1)
        elif self.type == "big_coin":
            car.collect_coin(10)
        elif self.type == "benzene":
            car.battery = min(car.battery + 10, car.MAX_BATTERY)
        elif self.type == "speed_boost":
           car.speed = min(car.speed + 1, car.MAX_SPEED)
        elif self.type == "nitro_boost":
            car.speed = min(car.speed * 1.5, car.MAX_SPEED)