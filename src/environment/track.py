from terrain import Terrain
from obs_reward import Obstacles
from obs_reward import Rewards
import random

class Track:
    def __init__(self, length):
        self.length = length
        self.segments = []
        self.init_track(length)
    
    def init_track(self,length):
        # loop till the end of the track
        # call random functions in terrain, obstacle, reward to make the segment
        for i in range(length):
            if i < length // 2: 
                segment_type = random.choice(['terrain', 'reward'])
            else:
                segment_type = random.choice(['terrain', 'obstacle', 'reward'])

            if segment_type == 'terrain':
                self.segments.append(Terrain.random_terrain())
            elif segment_type == 'obstacle':
                self.segments.append(Obstacles.random_obstacle())
            elif segment_type == 'reward':
                self.segments.append(Rewards.random_reward())
        return self.segments


    def get_segment(self,current_position):
        # return segment info
        if current_position < len(self.segments):
            return self.segments[current_position]
        else:
            return None