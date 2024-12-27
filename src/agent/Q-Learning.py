import sys
import os
import copy
import numpy as np
import random
import time 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.environment.envQ import Environment
from src.environment.terrain import Terrain
from src.environment.obs_reward import Obstacles
from src.environment.car import Car
from src.agent.visualize import Visualizer
import tracemalloc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



import random
import numpy as np

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

    fig, ax = plt.subplots()
    track_length = env.track.length
    positions = []

    def update(frame):
        nonlocal state, done
        ax.clear()

        if done:
            return

        if state not in q_table:
            action = random.choice(action_space)
        else:
            action = max(q_table[state], key=q_table[state].get)

        new_state, reward, done = env.step(action)

        positions.append(state[0])
        ax.plot(range(track_length), [0]*track_length, 'k-', lw=1)
        ax.plot(positions, [0]*len(positions), 'ro-', label='Agent Path')
        ax.set_xlim(-1, track_length)
        ax.set_ylim(-1, 1)
        ax.set_title(f"Action: {action}, Reward: {reward}")
        ax.legend()

        state = new_state 

        if done:
            ax.text(track_length // 2, 0.5, "Simulation End", fontsize=12, ha='center')
            ax.text(track_length // 2, -0.5, "Goal reached!" if state[0] >= track_length else "Failed.", fontsize=12, ha='center')

    ani = FuncAnimation(fig, update, frames=range(100), repeat=False, interval=500)
    plt.show()


env = Environment(track_length=10)
action_space = ["accelerate", "decelerate", "recharge", "move"]
q_table = q_learning(env, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1)
test_q_learning(q_table, env, action_space)
visualize_simulation(q_table, env, action_space)