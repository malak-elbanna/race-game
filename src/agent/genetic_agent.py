import sys
import os
import random
import copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car

# Fitness function to evaluate how close an agent is to the goal with respect to its utility (battery and speed)
def fitness(state, goal):
    position, speed, battery, coins = state
    return -(goal - position) + (battery / 100) * speed  

