from terrain import Terrain
from obs_reward import Obstacles
from obs_reward import Rewards
import random

class Track:
    def __init__(self, length):
        self.length = length
        self.init_track(length)
    
    def init_track(self,length):
        # loop till the end of the track
        # call random functions in terrain, obstacle, reward to make the segment
        segments = []
        for i in range(length):
            segment_type = random.choice(['terrain', 'obstacle', 'reward'])
            if segment_type == 'terrain':
                segments.append(Terrain.random_terrain())
            elif segment_type == 'obstacle':
                segments.append(Obstacles())
            elif segment_type == 'reward':
                segments.append(Rewards())
        return segments


    def get_segment(self,current_position):
        # return segment info
        if current_position < len(self.segments):
            return self.segments[current_position]
        else:
            return None