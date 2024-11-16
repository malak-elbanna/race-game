import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from src.agent.visualize import Visualizer
from collections import deque
import copy
import tracemalloc

def visualize_sol(solution, track_length):
    for position in solution:  
        if position >= track_length:
            track_length = position + 1

        track = ['_'] * track_length
        if position < track_length:
            track[position] = '🏎️'
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

def bfs(environment, goal, visualizer=None):
    initial_state = environment.get_state()
    frontier = deque([(initial_state, None, None)])
    visited = set()
    explored = []

    while frontier:
        state, parent, action = frontier.popleft()

        if visualizer and parent is not None:
            visualizer.add_state(parent, state, action)

        if state[0] >= goal:
            if visualizer:
                visualizer.add_state(parent, state, "goal")
            
            solution_path = [state]
            while parent:
                solution_path.append(parent)
                parent = next((p for s, p, _ in explored if s == parent), None)
            solution_path.reverse()
            return solution_path

        if environment.game_over():
            continue

        if state in visited:
            continue

        visited.add(state)
        path = [(state, 0)]
        successors = get_successors(environment, path)

        for new_state, i in successors:  
            if new_state not in visited:
                frontier.append((new_state, state, action))
                explored.append((new_state, state, action))

    return None  

def calc_avg_runtime():
    times = []
    for i in [5, 10, 15, 20, 25, 30, 35, 40]:
        env = Environment(track_length=i)
        start = time.time()
        solution = bfs(env, env.track.length -1)
        end = time.time()

        total = end - start
        times.append(total)
    
    avg_time = sum(times) / len(times)
    print("\nAverage time= ", avg_time)
    return avg_time


def calc_avg_memory():
    memory_usages = []

    for i in [5, 10, 15, 20, 25, 30, 35, 40]:
        env = Environment(track_length=i)
        
        tracemalloc.start()  
        sol = bfs(env, env.track.length - 1)
        current, peak = tracemalloc.get_traced_memory()  
        tracemalloc.stop()

        memory_usages.append(peak)  

    avg_memory = sum(memory_usages) / len(memory_usages)
    print("\nAverage memory usage (bytes):", avg_memory)
    return avg_memory
        

def main():
    env = Environment(track_length=10)  
    visualizer = Visualizer()
    solution = bfs(env, env.track.length - 1, visualizer)
    
    if solution:
        print("Solution path:", solution)
        total_steps = len(solution) - 1
        print("Total steps:", total_steps)
        
        positions = []
        for state in solution:
            positions.append(state[0])

        visualize_sol(positions, env.track.length)  

        visualizer.show_graph(solution)
    else:
        print("no solution")
        visualizer.show_graph()

main()
#calc_avg_runtime()
# calc_avg_memory