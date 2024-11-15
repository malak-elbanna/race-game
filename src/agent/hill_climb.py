import sys
import os
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
        track[position] = '🏎️'  
        print(''.join(track))
        time.sleep(0.5)  
    print("Goal Reached!")


def heuristic(state, goal):
    # heuristic will be the distance to the goal minus battery consumption
    # You can adjust this based on the goal; higher values mean a more favorable state
    position, speed, battery, coins = state
    return -(goal - position) + (battery / 100) * speed


def get_best_neighbor(environment, current_state, goal, visualizer=None):
    actions = ["accelerate", "decelerate", "recharge"]
    best_state = None
    best_heuristic = float('-inf')
    
    for action in actions:
        env_copy = copy.deepcopy(environment)
        env_copy.car.position = current_state[0]
        env_copy.car.speed = current_state[1]
        env_copy.car.battery = current_state[2]
        
        env_copy.step(action)
        new_state = env_copy.get_state()
        new_position = new_state[0]

        if new_position > current_state[0]: 
            state_heuristic = heuristic(new_state, goal)
            if state_heuristic > best_heuristic:
                best_heuristic = state_heuristic
                best_state = new_state

            if visualizer:
                visualizer.add_state(current_state, new_state, action)

    return best_state

def calc_avg_runtime():
    times = []
    for i in [5, 10, 15, 20, 25, 30, 35, 40]:
        env = Environment(track_length=i)
        start = time.time()
        solution = hill_climb(env, env.track.length -1)
        end = time.time()

        total = end - start
        times.append(total)
    
    avg_time = sum(times) / len(times)
    print("\nAverage time= ", avg_time)
    return avg_time

def hill_climb(environment, goal, visualizer=None):
    current_state = environment.get_state()
    path = [(current_state, 0)]
    
    while current_state[0] < goal:
        best_state = get_best_neighbor(environment, current_state, goal, visualizer)
        
        if not best_state or heuristic(best_state, goal) <= heuristic(current_state, goal):
            break  

        path.append((best_state, 1))
        current_state = best_state

    return path if current_state[0] >= goal else None

def main():
    env = Environment(track_length=10)  
    visualizer = Visualizer()
    solution = hill_climb(env, env.track.length - 1, visualizer)

    if solution:
        print("Solution path:", solution)
        print("Total steps:", len(solution) - 1)

        visualize(env, solution)
        visualizer.show_graph(solution)
    else:
        print("No solution found")
        visualizer.show_graph()

# main()
calc_avg_runtime()
