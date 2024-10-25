from enum import Enum
import numpy as np
from typing import Tuple, List, Dict
from dataclasses import dataclass
import random

class Action(Enum):
    ACCELERATE = 0
    DECELERATE = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    STOP = 4

class TerrainType(Enum):
    ROAD = 0          # Normal speed
    BOOST = 1         # Increased speed
    OBSTACLE = 2      # Decreased speed/damage
    RECHARGE = 3      # Fuel station
    WALL = 4          # Cannot pass
    FINISH = 5        # Goal state

@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

class RacingState:
    def __init__(self, size_x: int = 10, size_y: int = 20):
        """
        Initialize racing game state with a track of size_x width and size_y length
        """
        self.size_x = size_x
        self.size_y = size_y
        self.grid = np.zeros((size_x, size_y), dtype=int)
        
        # Car state
        self.position = Position(size_x // 2, 0)  # Start at bottom center
        self.speed = 0
        self.fuel = 100
        self.damage = 0
        self.time = 0
        
        # Game state
        self.game_over = False
        self.reached_goal = False
        
        # Initialize track with terrain
        self._initialize_track()
    
    def _initialize_track(self):
        """Create a track with various terrain types"""
        # Set basic road
        self.grid.fill(TerrainType.ROAD.value)
        
        # Add walls on the sides
        self.grid[0, :] = TerrainType.WALL.value
        self.grid[-1, :] = TerrainType.WALL.value
        
        # Add finish line
        self.grid[1:-1, -1] = TerrainType.FINISH.value
        
        # Add random obstacles (20% of track)
        n_obstacles = (self.size_x - 2) * (self.size_y - 1) // 5
        for _ in range(n_obstacles):
            x = random.randint(1, self.size_x - 2)
            y = random.randint(1, self.size_y - 2)
            self.grid[x, y] = TerrainType.OBSTACLE.value
        
        # Add boost pads (10% of track)
        n_boosts = (self.size_x - 2) * (self.size_y - 1) // 10
        for _ in range(n_boosts):
            x = random.randint(1, self.size_x - 2)
            y = random.randint(1, self.size_y - 2)
            if self.grid[x, y] == TerrainType.ROAD.value:
                self.grid[x, y] = TerrainType.BOOST.value
        
        # Add recharge stations (5% of track)
        n_recharge = (self.size_x - 2) * (self.size_y - 1) // 20
        for _ in range(n_recharge):
            x = random.randint(1, self.size_x - 2)
            y = random.randint(1, self.size_y - 2)
            if self.grid[x, y] == TerrainType.ROAD.value:
                self.grid[x, y] = TerrainType.RECHARGE.value

def transition_function(state: RacingState, action: Action) -> Tuple[RacingState, float, bool]:
    """
    Transition function that takes current state and action, returns (new_state, reward, done)
    
    Rewards:
    - Moving forward: +1 * speed
    - Reaching goal: +1000
    - Hitting obstacle: -50
    - Running out of fuel: -100
    - Using boost: +10
    - Recharging: -5 per fuel unit
    """
    new_state = RacingState(state.size_x, state.size_y)
    new_state.grid = state.grid.copy()
    new_state.position = Position(state.position.x, state.position.y)
    new_state.speed = state.speed
    new_state.fuel = state.fuel
    new_state.damage = state.damage
    new_state.time = state.time + 1
    
    # Process action
    if action == Action.ACCELERATE:
        new_state.speed = min(5, new_state.speed + 1)
        new_state.fuel -= 2
    elif action == Action.DECELERATE:
        new_state.speed = max(0, new_state.speed - 1)
        new_state.fuel -= 1
    elif action == Action.MOVE_LEFT:
        if new_state.position.x > 1:  # Avoid wall
            new_state.position.x -= 1
        new_state.fuel -= 1
    elif action == Action.MOVE_RIGHT:
        if new_state.position.x < state.size_x - 2:  # Avoid wall
            new_state.position.x += 1
        new_state.fuel -= 1
    elif action == Action.STOP:
        new_state.speed = 0
        new_state.fuel -= 0.5
    
    # Move forward based on speed
    new_state.position.y = min(state.size_y - 1, 
                             new_state.position.y + new_state.speed)
    
    # Check current terrain
    current_terrain = TerrainType(new_state.grid[new_state.position.x, new_state.position.y])
    reward = new_state.speed  # Base reward for moving forward
    
    # Process terrain effects
    if current_terrain == TerrainType.BOOST:
        new_state.speed = min(5, new_state.speed + 2)
        reward += 10
    elif current_terrain == TerrainType.OBSTACLE:
        new_state.speed = max(0, new_state.speed - 2)
        new_state.damage += 20
        reward -= 50
    elif current_terrain == TerrainType.RECHARGE:
        missing_fuel = 100 - new_state.fuel
        new_state.fuel = 100
        reward -= missing_fuel * 0.5  # Cost of recharging
    elif current_terrain == TerrainType.FINISH:
        new_state.reached_goal = True
        reward += 1000
        return new_state, reward, True
    
    # Check game over conditions
    if (new_state.fuel <= 0 or new_state.damage >= 100):
        new_state.game_over = True
        reward -= 100
        return new_state, reward, True
    
    return new_state, reward, False

def estimate_state_space_size(size_x: int = 10, size_y: int = 20) -> int:
    """
    Estimate the state space size:
    - Position: size_x * size_y positions
    - Speed: 6 possible speeds (0-5)
    - Fuel: Discretized to 20 levels
    - Damage: Discretized to 20 levels
    """
    positions = size_x * size_y
    speeds = 6
    fuel_levels = 20
    damage_levels = 20
    
    total_states = positions * speeds * fuel_levels * damage_levels
    return total_states

# Example usage
def example_game():
    state = RacingState()
    print(f"Estimated state space size: {estimate_state_space_size()}")
    print("\nInitial state:")
    print(f"Position: ({state.position.x}, {state.position.y})")
    print(f"Speed: {state.speed}")
    print(f"Fuel: {state.fuel}")
    
    # Make some moves
    actions = [Action.ACCELERATE, Action.MOVE_RIGHT, Action.ACCELERATE]
    for action in actions:
        next_state, reward, done = transition_function(state, action)
        print(f"\nAction: {action.name}")
        print(f"Reward: {reward}")
        print(f"New position: ({next_state.position.x}, {next_state.position.y})")
        print(f"New speed: {next_state.speed}")
        print(f"New fuel: {next_state.fuel}")
        print(f"Game Over: {done}")
        if done:
            break
        state = next_state

if __name__ == "__main__":
    example_game()