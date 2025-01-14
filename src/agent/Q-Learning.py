import sys
import os
import copy
import numpy as np
import random
import time 
import tracemalloc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.envQ import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from src.agent.visualize import Visualizer
import tracemalloc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def q_learning(env, episodes, alpha=0.1, gamma=0.9, epsilon=0.1):
    Q = {}  # Initialize the Q-table as a dictionary
    actions = ["accelerate", "decelerate", "recharge", "move"]

    for episode in range(episodes):
        state = env.get_state()  # Get the initial state
        done = False

        while not done:
            # Ensure state exists in Q-table
            if state not in Q:
                Q[state] = {action: 0 for action in actions}

            # Epsilon-greedy policy
            if random.uniform(0, 1) < epsilon:
                action = random.choice(actions)  # Explore: a random action
            else:
                # Exploit: take the action with the highest Q-value
                action = max(Q[state], key=Q[state].get)

            # Take the action
            new_state, reward, done = env.step(action)

            # Ensure the new state exists in the Q-table
            if new_state not in Q:
                Q[new_state] = {action: 0 for action in actions}

            # Get the maximum future Q-value for the new state
            max_future_q = max(Q[new_state].values())

            # Update the Q-value for the current state-action pair
            Q[state][action] += alpha * (reward + gamma * max_future_q - Q[state][action])

            # Move to the next state
            state = new_state

    return Q

def test_q_learning(q_table, env, action_space):
    env.rebuild()  # Reset the environment
    state = env.get_state()  # Get the initial state
    done = False

    while not done:
        # Ensure the state exists in the Q-table
        if state not in q_table:
            print("State not found in Q-table, taking random action.")
            action = random.choice(action_space)
        else:
            # Select the best action from Q-table
            action = max(q_table[state], key=q_table[state].get) 

        new_state, reward, done = env.step(action)
        print(f"State: {new_state}, Reward: {reward}, Action: {action}")

        state = new_state  

    if state[0] >= env.track.length:
        print("Goal reached!")
    else:
        print("Failed.")

def visualize_simulation(q_table, env, action_space):
    env.rebuild() 
    state = env.get_state() 
    done = False
    
    # Collect all positions first
    positions = []
    states = []
    actions = []
    rewards = []
    
    while not done:
        if state not in q_table:
            action = random.choice(action_space)
        else:
            action = max(q_table[state], key=q_table[state].get)
            
        new_state, reward, done = env.step(action)
        positions.append(state[0])
        states.append(state)
        actions.append(action)
        rewards.append(reward)
        state = new_state
        
    # Add final position
    positions.append(state[0])
    
    # Create figure and animation
    fig, ax = plt.subplots(figsize=(10, 6))
    track_length = env.track.length
    
    def update(frame):
        ax.clear()
        
        ax.plot(range(track_length), [0]*track_length, 'k-', lw=1)
        
        current_positions = positions[:frame+1]
        ax.plot(current_positions, [0]*len(current_positions), 'ro-', label='Agent Path')
        
        ax.set_xlim(-1, track_length + 1)
        ax.set_ylim(-1, 1)
        
        if frame < len(actions):
            ax.set_title(f"Step {frame}: Action: {actions[frame]}, Reward: {rewards[frame]:.2f}")
        
        if frame == len(positions) - 1:
            status = "Goal reached!" if positions[-1] >= track_length else "Failed"
            ax.text(track_length/2, 0.5, f"Simulation End - {status}", 
                   fontsize=12, ha='center', bbox=dict(facecolor='white', alpha=0.7))
        
        ax.grid(True)
        ax.legend()
        
    num_frames = len(positions)
    ani = FuncAnimation(fig, update, frames=num_frames, 
                       interval=500, repeat=False)
    
    plt.show()

env = Environment(track_length=10)
action_space = ["accelerate", "decelerate", "recharge", "move"]
q_table = q_learning(env, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1)

tracemalloc.start()
startTime = time.time()

test_q_learning(q_table, env, action_space)

endtime = time.time()
current,most = tracemalloc.get_traced_memory()
totaltime = endtime-startTime
visualize_simulation(q_table, env, action_space)

print("Current is : " , current)
print ("Most is : " , most)
print ("Total time is : " , totaltime)

tracemalloc.stop()
