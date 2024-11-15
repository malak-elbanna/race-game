import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from collections import deque
import copy

def visualize(solution, track_length):
    for step in solution:
        state = step[0]
        position = state[0]

        if position >= track_length:
            track_length = position + 1

        track = ['_'] * track_length
        if position < track_length:
            track[position] = 'C'
        print(''.join(track))

        time.sleep(0.5)
    print("Goal Reached!")

def get_successors(environment, path):
    actions = ["accelerate", "decelerate", "recharge", "move"]
    state = path[-1][0]
    position = state[0]
    successors = []

    for action in actions:
        env_copy = copy.deepcopy(environment)
        env_copy.car.position = position
        env_copy.car.speed = state[1]
        env_copy.car.battery = state[2]

        env_copy.step(action)
        new_state = env_copy.get_state()
        new_position = new_state[0]

        if new_position > position:
            successors.append((new_state, 1))
    return successors

def dfs(environment, goal):
    initial_state = environment.get_state()
    frontier = deque([[(initial_state, 0)]])  
    visited = set()

    while frontier:
        path = frontier.pop() 
        state = path[-1][0]

        if state[0] >= goal:
            return path

        if environment.game_over():
            continue

        if state in visited:
            continue

        visited.add(state)
        successors = get_successors(environment, path)

        for new_state, i in successors:
            if new_state not in visited:
                new_path = path + [(new_state, 1)]
                frontier.append(new_path)

    return None

def main():
    env = Environment(track_length=40)
    solution = dfs(env, env.track.length - 1)

    if solution:
        print("Solution path:", solution)
        total_steps = len(solution) - 1
        print("Total steps:", total_steps)
        visualize(solution, env.track.length)
    else:
        print("No solution")

main()
