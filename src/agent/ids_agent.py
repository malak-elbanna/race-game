import sys
import os
import time  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from collections import deque

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

def get_successors(environment, path):
    actions = ["accelerate", "decelerate", "recharge", "move"]
    state = path[-1][0]
    position = state[0]
    successors = []
    seen_states = set()

    for action in actions:
        environment.car.position = position
        environment.car.speed = state[1]
        environment.car.battery = state[2]

        environment.step(action)
        new_state = environment.get_state()
        new_position = new_state[0]

        if new_position > position and new_state not in seen_states:
            successors.append((new_state, 1))
            seen_states.add(new_state)
    return successors

def dfs_limited(environment, goal, limit):
    initial_state = environment.get_state()
    frontier = deque([[(initial_state, 0)]]) 
    visited = set()  

    while frontier:
        path = frontier.pop()
        state = path[-1][0]

        if state[0] >= goal:
            return path

        if len(path) - 1 >= limit:
            continue

        if environment.game_over():
            continue

        if state in visited:
            continue

        visited.add(state)
        successors = get_successors(environment, path)

        for new_state, _ in successors:
            if new_state not in visited:
                new_path = path + [(new_state, 1)]
                frontier.append(new_path)

    return None

def ids(environment, goal):
    depth = 0
    while True:
        result = dfs_limited(environment, goal, depth)
        if result:
            return result
        depth += 1

def main():
    env = Environment(track_length=40)
    solution = ids(env, env.track.length - 1)

    if solution:
        print("Solution path:", solution)
        total_steps = len(solution) - 1
        print("Total steps:", total_steps)
        visualize(env, solution)  
    else:
        print("No solution")

main()
