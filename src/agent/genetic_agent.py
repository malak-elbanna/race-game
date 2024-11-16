import sys
import os
import random
import copy
import time
import tracemalloc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.agent.astar_agent import astar
from src.agent.hill_climb import hill_climb
from src.agent.simulated_annealing import simulated_annealing
from src.agent.dfs_agent import dfs
from src.agent.gbfs_agent import greedy
from src.agent.visualize import Visualizer

def fitness(path):
    return len(path) - 1  

def reproduce(parent1, parent2):
    cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:cut] + parent2[cut:]
    child2 = parent2[:cut] + parent1[cut:]
    return child1, child2

def mutate(path, environment):
    if len(path) < 2:
        return path
    index = random.randint(0, len(path) - 2)
    state = path[index][0]
    actions = ["accelerate", "decelerate", "recharge", "move"]
    mutated_path = copy.deepcopy(path[:index+1])
    
    env_copy = copy.deepcopy(environment)
    env_copy.car.position = state[0]
    env_copy.car.speed = state[1]
    env_copy.car.battery = state[2]
    
    env_copy.step(random.choice(actions))
    mutated_path.append((env_copy.get_state(), 1))

    return mutated_path


def visualize_genetic_algorithm(environment, path, visualizer):
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
    visualizer.show_graph()

def calc_avg_runtime():
    times = []
    for i in [5, 10, 15, 20, 25, 30, 35, 40]:
        env = Environment(track_length=i)
        start = time.time()
        visualizer = Visualizer()
        solution = genetic_algorithm(env, i - 1, visualizer=visualizer)
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
        visualizer = Visualizer()
        sol = genetic_algorithm(env, i - 1, visualizer=visualizer)
        current, peak = tracemalloc.get_traced_memory()  
        tracemalloc.stop()

        memory_usages.append(peak)  

    avg_memory = sum(memory_usages) / len(memory_usages)
    print("\nAverage memory usage (bytes):", avg_memory)
    return avg_memory 
def genetic_algorithm(environment, goal, generations=100, visualizer=None):
    population = [
        astar(environment, goal),
        hill_climb(environment, goal),
        simulated_annealing(environment, goal),
        greedy(environment, goal)
    ]

    best_solution = None
    best_fitness = float('inf')

    for gen in range(generations):
        print(f"Generation {gen + 1}")

        scores = [(path, fitness(path)) for path in population]

        for path, score in scores:
            if path and path[-1][0][0] == goal and score < best_fitness:
                best_solution = path
                best_fitness = score

        population.sort(key=fitness)
        selected = population[:2]

        # Reproduce 
        child1, child2 = reproduce(selected[0], selected[1])

        # Mutation
        child1 = mutate(child1, environment)
        child2 = mutate(child2, environment)

        # Update population with the new generation
        population = [selected[0], selected[1], child1, child2]

        # Track the state transitions with the visualizer if provided
        if visualizer:
            for path in [selected[0], selected[1], child1, child2]:
                if len(path) > 1:
                    for i in range(len(path) - 1):
                        parent = path[i][0]
                        child = path[i + 1][0]
                        action = "Mutate" if path == child1 or path == child2 else "Reproduce"
                        visualizer.add_state(parent, child, action)

    if visualizer: 
        visualizer.show_graph()

    return best_solution


env = Environment(track_length=10)  
visualizer = Visualizer()  
solution = genetic_algorithm(env, env.track.length - 1, generations=100, visualizer=visualizer)  # Pass visualizer here

print("Solution path:", solution)
print("Total steps:", len(solution) - 1)
    
# Optionally visualize the final solution path
visualize_genetic_algorithm(env, solution, visualizer)