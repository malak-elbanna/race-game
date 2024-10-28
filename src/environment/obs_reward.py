import random

class Obstacles:
    obs = ["wall", "animal",'mud']

    def __init__(self, obstacle):
        self.type = obstacle
        self.impact = self.impact(obstacle)
    @classmethod
    def random_obstacle(cls):
        # Randomly select an obstacle type
        obstacle = random.choice(cls.obs_types)
        return cls(obstacle)
    
    def impact(self,car):
        if self.obstacle == "wall":
            pass # here is code to stop the car
        elif self.obstacle == "animal":
            car.decelerate()
        elif self.obstacle == "mud":
            car.decelerate()

class Rewards:
    rews = ["small_coin",'big_coin', "benzene",'speed_boost','nitro_boost']

    def __init__(self, reward):
        self.reward = reward
        self.impact = self.impact(reward)
    
    @classmethod
    def random_reward(cls):
        # Randomly select a reward type
        reward = random.choice(cls.reward_types)
        return cls(reward)

    def impact(self,car):
        if self.reward == "small_coin":
            car.collect_coin(1)
        elif self.reward == "big_coin":
            car.collect_coin(10)
        elif self.reward == "benzene":
            car.recharge()
        elif self.reward == "speed_boost":
            car.accelerate()
        elif self.reward == "nitro_boost":
            pass # double speed temporarily 