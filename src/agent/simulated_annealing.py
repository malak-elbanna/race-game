import sys
import os
import math
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
import copy

def heuristic(state, goal):
    # heuristic will be the distance to the goal minus battery consumption
    # You can adjust this based on the goal; higher values mean a more favorable state
    position, speed, battery, coins = state
    return -(goal - position) + (battery / 100) * speed


def get_random_neighbor(environment, current_state):
    # Select a random successor by applying a random action
    actions = ["accelerate", "decelerate", "recharge"]
    action = random.choice(actions)
    
    env_copy = copy.deepcopy(environment)
    env_copy.car.position = current_state[0]
    env_copy.car.speed = current_state[1]
    env_copy.car.battery = current_state[2]
    
    env_copy.step(action)
    new_state = env_copy.get_state()
    
    return new_state

def simulated_annealing(environment, goal, initial_temp=1000):
    current_state = environment.get_state()  
    temperature = initial_temp
    path = [(current_state, 0)]

    while temperature > 0:
        if current_state[0] >= goal:
            return path  

        next_state = get_random_neighbor(environment, current_state)
        
        # Calculate energy difference (ΔE = VALUE(current) - VALUE(next))
        current_heuristic = heuristic(current_state, goal)
        next_heuristic = heuristic(next_state, goal)
        delta_e = next_heuristic - current_heuristic
        
        # Acceptance criteria
        if delta_e > 0:
            # If next state is better, accept it
            current_state = next_state
            path.append((next_state, 1))
        else:
            # Accept worse state with probability e^(-ΔE / T)
            if random.random() < math.exp(-delta_e / temperature):
                current_state = next_state
                path.append((next_state, 1))
        
        # decrease the temperature
        temperature -= 5

    return path if current_state[0] >= goal else None

env = Environment(track_length=10)  
solution = simulated_annealing(env, env.track.length - 1)

print("Solution path:", solution)
print("Total steps:", len(solution) - 1)