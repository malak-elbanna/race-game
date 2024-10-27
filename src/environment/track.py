from terrain import Terrain
from obs_rewards import Obstacles
from obs_rewards import Rewards

class Track:
    def __init__(self, length):
        self.length = length
        self.segments = []
        self.init_track()
    
    def init_track(self):
        # loop till the end of the track
        # call random functions in terrain, obstacle, reward to make the segment
        pass

    def get_segments(self):
        # return segment info
        pass