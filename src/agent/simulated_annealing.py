import sys
import os
import math
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from src.agent.visualize import Visualizer
import copy
import time 



def visualize(environment, path):
    track_length = environment.track.length  
    for step in path:
        state = step[0]
        position = state[0]
        
        if position >= track_length:
            track_length = position + 1
        
        track = ['_'] * track_length
        track[position] = 'C'  
        print(''.join(track))
        time.sleep(0.5) 
    print("Goal Reached!")



def heuristic(state, goal):
    # heuristic will be the distance to the goal minus battery consumption
    # You can adjust this based on the goal; higher values mean a more favorable state
    position, speed, battery, coins = state
    return -(goal - position) + (battery / 100) * speed


def get_random_neighbor(environment, current_state, visualizer=None):
    actions = ["accelerate", "decelerate", "recharge"]
    action = random.choice(actions)
    
    env_copy = copy.deepcopy(environment)
    env_copy.car.position = current_state[0]
    env_copy.car.speed = current_state[1]
    env_copy.car.battery = current_state[2]
    
    env_copy.step(action)
    new_state = env_copy.get_state()

    if visualizer:
        visualizer.add_state(current_state, new_state, action)

    return new_state

def simulated_annealing(environment, goal, visualizer=None, initial_temp=1000):
    current_state = environment.get_state()  
    temperature = initial_temp
    path = [(current_state, 0)]

    while temperature > 0:
        if current_state[0] >= goal:
            return path  

        next_state = get_random_neighbor(environment, current_state, visualizer)
        
        current_heuristic = heuristic(current_state, goal)
        next_heuristic = heuristic(next_state, goal)
        delta_e = next_heuristic - current_heuristic
        
        if delta_e > 0:
            current_state = next_state
            path.append((next_state, 1))
        else:
            if random.random() < math.exp(-delta_e / temperature):
                current_state = next_state
                path.append((next_state, 1))
        
        # Decrease temperature
        temperature -= 5

    return path if current_state[0] >= goal else None

def main():
    env = Environment(track_length=10)  
    visualizer = Visualizer()  
    solution = simulated_annealing(env, env.track.length - 1, visualizer)

    if solution:
        print("Solution path:", solution)
        print("Total steps:", len(solution) - 1)
        
        visualizer.show_graph(solution)
    else:
        print("No solution found")
        visualizer.show_graph()

main()

