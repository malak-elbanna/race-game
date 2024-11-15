import sys
import os
import copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from src.agent.visualize import Visualizer
import heapq
import time
import tracemalloc

def visualize(solution, track_length):
    for step in solution:
        state = step[0]
        position = state[0]

        if position >= track_length:
            track_length = position + 1

        track = ['_'] * track_length
        if position < track_length:
            track[position] = '🏎️'
        print(''.join(track))

        time.sleep(0.5)
    print("Goal Reached!")

def path_cost(path):
    g_cost = 0
    for _, cost in path:
        g_cost += cost
    return g_cost

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
            segment = env_copy.track.get_segment(new_position)
            cost = 1
            new_speed = new_state[1]

            if isinstance(segment, Terrain):
                cost += max(1, new_speed * segment.get_mult())
            elif isinstance(segment, Obstacles):
                cost += max(1, new_speed * 1.5)

            successors.append((new_state, cost))
    return successors

def ucs(environment, goal, visualizer=None):
    initial_state = environment.get_state()
    frontier = []
    heapq.heappush(frontier, (0, [(initial_state, 0)]))  
    visited = {}

    while frontier:
        g_cost, path = heapq.heappop(frontier)
        state = path[-1][0]
        
        if state[0] >= goal:
            return path

        if environment.game_over():
            continue

        if state in visited and visited[state] <= g_cost:
            continue

        visited[state] = g_cost

        successors = get_successors(environment, path)
        for new_state, cost in successors:
            if visualizer:
                visualizer.add_state(state, new_state, action="move")

            new_path = path + [(new_state, cost)]
            new_g_cost = path_cost(new_path)
            if new_state not in visited or visited[new_state] > new_g_cost:
                heapq.heappush(frontier, (new_g_cost, new_path))

    return None  

def calc_avg_runtime():
    times = []
    for i in [5, 10, 15, 20, 25, 30, 35, 40]:
        env = Environment(track_length=i)
        start = time.time()
        solution = ucs(env, env.track.length -1)
        end = time.time()

        total = end - start
        times.append(total)
    
    avg_time = sum(times) / len(times)
    print("\nAverage time= ", avg_time)
    return avg_time

def calc_avg_memory():
    memory_usages = []

    for i in [5, 10, 15, 20, 25, 30]:
        env = Environment(track_length=i)
        
        tracemalloc.start()  
        sol = ucs(env, env.track.length - 1)
        current, peak = tracemalloc.get_traced_memory()  
        tracemalloc.stop()

        memory_usages.append(peak)  

    avg_memory = sum(memory_usages) / len(memory_usages)
    print("\nAverage memory usage (bytes):", avg_memory)
    return avg_memory

def main():
    env = Environment(track_length=20)
    print(env)  
    visualizer = Visualizer()
    solution = ucs(env, env.track.length - 1, visualizer)

    if solution:
        print("Solution path:", solution)
        total_cost = 0
        for _, cost in solution:
            total_cost += cost

        print("Total cost: ", total_cost)

        visualize(solution, env.track.length)
        visualizer.show_graph(solution)
    else:
        print("No solution")
        visualizer.show_graph()

# main()
#calc_avg_runtime()

calc_avg_memory()