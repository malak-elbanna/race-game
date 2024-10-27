import random

class Obstacles:
    obs = ["wall", "animal", None]

    def __init__(self, obstacle):
        self.type = obstacle
        self.impact = impact(obstacle)

    def random_obstacle(self):
        pass
    
    def impact(self):
        # impact of obstacle on car
        # ig if conditions
        pass

class Rewards:
    rews = ["coin", "benzene", None]

    def __init__(self, reward):
        self.reward = reward
        self.impact = impact(reward)
    
    def random_reward(self):
        pass

    def impact(self):
        # impact of reward on car
        # ig if conditions
        pass