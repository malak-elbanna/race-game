import numpy as np
from typing import Tuple, List, Dict
from enum import Enum

class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class GameState:
    def __init__(self, size: int = 4):
        """
        Initialize game state with a small grid (default 4x4)
        0 = empty, 1 = snake body, 2 = food
        """
        self.size = size
        self.grid = np.zeros((size, size))
        
        # Initialize snake in the middle
        self.snake_positions = [(size//2, size//2)]
        self.grid[size//2, size//2] = 1
        
        # Place food randomly
        self.place_food()
        
        self.game_over = False
        self.score = 0
    
    def place_food(self):
        """Place food in a random empty cell"""
        empty_cells = list(zip(*np.where(self.grid == 0)))
        if empty_cells:
            food_pos = empty_cells[np.random.randint(len(empty_cells))]
            self.grid[food_pos] = 2
    
    def get_next_head_position(self, action: Action) -> Tuple[int, int]:
        """Calculate next head position based on action"""
        curr_head = self.snake_positions[0]
        if action == Action.UP:
            return (curr_head[0]-1, curr_head[1])
        elif action == Action.RIGHT:
            return (curr_head[0], curr_head[1]+1)
        elif action == Action.DOWN:
            return (curr_head[0]+1, curr_head[1])
        else:  # LEFT
            return (curr_head[0], curr_head[1]-1)

def transition_function(state: GameState, action: Action) -> Tuple[GameState, int, bool]:
    """
    Transition function that takes current state and action, returns (new_state, reward, done)
    
    Rewards:
    - Eating food: +10
    - Moving: +0
    - Game over: -10
    """
    new_state = GameState(state.size)
    new_state.grid = state.grid.copy()
    new_state.snake_positions = state.snake_positions.copy()
    new_state.score = state.score
    
    # Get new head position
    new_head = new_state.get_next_head_position(action)
    
    # Check if game over
    if (new_head[0] < 0 or new_head[0] >= state.size or
        new_head[1] < 0 or new_head[1] >= state.size or
        new_state.grid[new_head] == 1):
        new_state.game_over = True
        return new_state, -10, True
    
    # Check if food found
    ate_food = new_state.grid[new_head] == 2
    
    # Move snake
    new_state.snake_positions.insert(0, new_head)
    new_state.grid[new_head] = 1
    
    if not ate_food:
        # Remove tail if no food eaten
        tail = new_state.snake_positions.pop()
        new_state.grid[tail] = 0
    else:
        # Increment score and place new food
        new_state.score += 1
        new_state.place_food()
        return new_state, 10, False
    
    return new_state, 0, False

# Example usage
def example_game():
    state = GameState(4)
    print("Initial state:")
    print(state.grid)
    
    # Make some moves
    actions = [Action.RIGHT, Action.DOWN, Action.LEFT]
    for action in actions:
        next_state, reward, done = transition_function(state, action)
        print(f"\nAction: {action.name}")
        print(f"Reward: {reward}")
        print(f"Game Over: {done}")
        print(next_state.grid)
        if done:
            break
        state = next_state

if __name__ == "__main__":
    example_game()