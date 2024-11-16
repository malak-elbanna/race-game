import sys
import os
import random
import copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.env import Environment
from src.agent.astar_agent import astar
from src.agent.hill_climb import hill_climb
from src.agent.simulated_annealing import simulated_annealing
from src.agent.dfs_agent import dfs
from src.agent.gbfs_agent import greedy
import time
import tracemalloc

def fitness(path):
    # fitness function that returns the length of the path, Shorter paths are more fit
    return len(path) - 1  

def reproduce(parent1, parent2):
    # Perform reproducing by combining parts of two paths
    cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:cut] + parent2[cut:]
    child2 = parent2[:cut] + parent1[cut:]
    return child1, child2

def mutate(path,environment):
    # Mutate(child) with small random probability
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
    
    # Randomly select an action and apply it for mutation
    env_copy.step(random.choice(actions))
    mutated_path.append((env_copy.get_state(), 1))  # Add mutated state

    return mutated_path

def genetic_algorithm(environment, goal, generations=100):
    # Initialize population with four search techniques we already made (A*, Hill Climb, Simulated Annealing, DFS)
    population = [
        astar(environment, goal),
        hill_climb(environment, goal),
        simulated_annealing(environment, goal),
        greedy(environment, goal)
    ]

    # To remember which is the best solution found
    best_solution = None
    best_fitness = float('inf')

    for gen in range(generations):
        print(f"Generation {gen + 1}")

        # Calculate fitness for each individual
        scores = [(path, fitness(path)) for path in population]

        # Check for improvements in best solution
        for path, score in scores:
            if path and path[-1][0][0] == goal and score < best_fitness:
                best_solution = path
                best_fitness = score

        # Selection
        population.sort(key=fitness)
        selected = population[:2]

        # Reproduce 
        child1, child2 = reproduce(selected[0], selected[1])

        # Mutation
        child1 = mutate(child1,environment)
        child2 = mutate(child2,environment)

        # Update population with the new generation
        population = [selected[0], selected[1], child1, child2]

    return best_solution

def calc_avg_runtime():
    times = []
    for i in [5, 10, 15, 20, 25, 30, 35, 40]:
        env = Environment(track_length=i)
        start = time.time()
        solution = genetic_algorithm(env, i -1)
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
        sol = genetic_algorithm(env, i - 1)
        current, peak = tracemalloc.get_traced_memory()  
        tracemalloc.stop()

        memory_usages.append(peak)  

    avg_memory = sum(memory_usages) / len(memory_usages)
    print("\nAverage memory usage (bytes):", avg_memory)
    return avg_memory 

# Usage example
# env = Environment(track_length=100)
# goal = env.track.length - 1
# solution = genetic_algorithm(env, goal)

# print("Best solution that the genetic algorithm found:\n", solution)

#calc_avg_runtime()
calc_avg_memory()
