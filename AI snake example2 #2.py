from enum import Enum
import numpy as np
from typing import Tuple, List, Dict, Set
from dataclasses import dataclass
from collections import deque
import random

class Action(Enum):
    ACCELERATE = 0
    DECELERATE = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    STOP = 4

@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

@dataclass
class State:
    position: Position
    speed: int
    fuel: float
    damage: float
    
    def __hash__(self):
        return hash((self.position, self.speed, int(self.fuel), int(self.damage)))
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.position == other.position and 
                self.speed == other.speed and 
                int(self.fuel) == int(other.fuel) and 
                int(self.damage) == int(other.damage))

class RacingGame:
    def __init__(self, size_x: int = 10, size_y: int = 20):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = np.zeros((size_x, size_y), dtype=int)
        self._initialize_track()
        
        # Initial state
        self.initial_state = State(
            position=Position(size_x // 2, 0),
            speed=0,
            fuel=100,
            damage=0
        )
    
    def _initialize_track(self):
        """Initialize track with terrain (same as before)"""
        # Same initialization as in your previous code
        self.grid.fill(0)  # Road
        self.grid[0, :] = 4  # Walls
        self.grid[-1, :] = 4
        self.grid[1:-1, -1] = 5  # Finish line
        
        # Add obstacles
        n_obstacles = (self.size_x - 2) * (self.size_y - 1) // 5
        for _ in range(n_obstacles):
            x = random.randint(1, self.size_x - 2)
            y = random.randint(1, self.size_y - 2)
            self.grid[x, y] = 2
        
        # Add boosts
        n_boosts = (self.size_x - 2) * (self.size_y - 1) // 10
        for _ in range(n_boosts):
            x = random.randint(1, self.size_x - 2)
            y = random.randint(1, self.size_y - 2)
            if self.grid[x, y] == 0:
                self.grid[x, y] = 1

    def is_goal_state(self, state: State) -> bool:
        """Check if current state is a goal state"""
        return self.grid[state.position.x, state.position.y] == 5

    def get_valid_actions(self, state: State) -> List[Action]:
        """Get list of valid actions from current state"""
        valid_actions = [Action.STOP]
        
        # Can always accelerate/decelerate unless at min/max speed
        if state.speed < 5:
            valid_actions.append(Action.ACCELERATE)
        if state.speed > 0:
            valid_actions.append(Action.DECELERATE)
        
        # Can move left/right if not at edges and have fuel
        if state.position.x > 1 and state.fuel >= 1:
            valid_actions.append(Action.MOVE_LEFT)
        if state.position.x < self.size_x - 2 and state.fuel >= 1:
            valid_actions.append(Action.MOVE_RIGHT)
                
        return valid_actions

    def transition(self, state: State, action: Action) -> Tuple[State, float, bool]:
        """Apply action to state and return (new_state, reward, done)"""
        new_state = State(
            Position(state.position.x, state.position.y),
            state.speed,
            state.fuel,
            state.damage
        )
        
        # Apply action effects
        if action == Action.ACCELERATE:
            new_state.speed = min(5, new_state.speed + 1)
            new_state.fuel -= 2
        elif action == Action.DECELERATE:
            new_state.speed = max(0, new_state.speed - 1)
            new_state.fuel -= 1
        elif action == Action.MOVE_LEFT:
            new_state.position.x -= 1
            new_state.fuel -= 1
        elif action == Action.MOVE_RIGHT:
            new_state.position.x += 1
            new_state.fuel -= 1
        elif action == Action.STOP:
            new_state.speed = 0
            new_state.fuel -= 0.5
        
        # Move forward based on speed
        new_state.position.y = new_state.position.y + new_state.speed
        
        # Check if game is over
        done = (new_state.fuel <= 0 or 
                new_state.damage >= 100 or 
                self.is_goal_state(new_state))
        
        # Calculate reward
        reward = new_state.speed  # Base reward for movement
        
        # Additional rewards based on terrain
        terrain = self.grid[new_state.position.x, new_state.position.y]
        if terrain == 1:  # Boost
            reward += 10
            new_state.speed = min(5, new_state.speed + 2)
        elif terrain == 2:  # Obstacle
            reward -= 50
            new_state.damage += 20
            new_state.speed = max(0, new_state.speed - 2)
        elif terrain == 5:  # Finish line
            reward += 1000
        
        return new_state, reward, done

def bfs_search(game: RacingGame) -> List[Action]:
    """
    Use BFS to find a path to the goal state
    Returns list of actions to reach goal
    """
    start_state = game.initial_state
    queue = deque([(start_state, [])])  # (state, actions_to_reach)
    visited = set()
    
    while queue:
        current_state, actions = queue.popleft()
        
        if current_state in visited:
            continue
            
        visited.add(current_state)
        
        # Check if we've reached the goal
        if game.is_goal_state(current_state):
            return actions
        
        # Try each valid action
        for action in game.get_valid_actions(current_state):
            next_state, reward, done = game.transition(current_state, action)
            
            # Only add to queue if state is valid
            if (next_state.fuel > 0 and 
                next_state.damage < 100 and 
                next_state not in visited):
                queue.append((next_state, actions + [action]))
    
    return []  # No path found

def main():
    # Create game instance
    game = RacingGame(size_x=10, size_y=20)
    
    # Find path using BFS
    path = bfs_search(game)
    
    if not path:
        print("No path found!")
        return
    
    print("Found path to goal:")
    
    # Follow the path and show states
    current_state = game.initial_state
    total_reward = 0
    
    print("\nInitial state:")
    print(f"Position: ({current_state.position.x}, {current_state.position.y})")
    print(f"Speed: {current_state.speed}")
    print(f"Fuel: {current_state.fuel}")
    
    for action in path:
        next_state, reward, done = game.transition(current_state, action)
        total_reward += reward
        
        print(f"\nAction: {action.name}")
        print(f"New position: ({next_state.position.x}, {next_state.position.y})")
        print(f"Speed: {next_state.speed}")
        print(f"Fuel: {next_state.fuel}")
        print(f"Reward: {reward}")
        
        if done:
            print("\nReached goal state!")
            break
            
        current_state = next_state
    
    print(f"\nTotal reward: {total_reward}")
    print(f"Path length: {len(path)}")

if __name__ == "__main__":
    main()