import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import clear_output
from collections import deque
from dataclasses import dataclass

# Constants for terrain types
ROAD, BOOST, OBSTACLE, AGENT, WALL, FINISH_LINE = 0, 1, 2, 3, 4, 5

@dataclass
class Position:
    x: int
    y: int

@dataclass
class State:
    position: Position
    speed: int
    fuel: int
    damage: int

@dataclass
class Action:
    dx: int
    dy: int
    change_speed: int

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
        # Initialize track with terrain, walls, finish line, obstacles, and boosts
        self.grid.fill(ROAD)  # Road
        self.grid[0, :] = WALL  # Top wall
        self.grid[-1, :] = WALL  # Bottom wall
        self.grid[1:-1, -1] = FINISH_LINE  # Finish line on the right side

        # Random obstacles and boosts
        n_obstacles = (self.size_x - 2) * (self.size_y - 1) // 5
        n_boosts = (self.size_x - 2) * (self.size_y - 1) // 10

        for _ in range(n_obstacles):
            x, y = random.randint(1, self.size_x - 2), random.randint(1, self.size_y - 2)
            self.grid[x, y] = OBSTACLE

        for _ in range(n_boosts):
            x, y = random.randint(1, self.size_x - 2), random.randint(1, self.size_y - 2)
            if self.grid[x, y] == ROAD:
                self.grid[x, y] = BOOST

    def visualize_state(self, state: State):
        """Visualize the current state of the game."""
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(8, 16))

        for x in range(self.size_x):
            for y in range(self.size_y):
                color = 'white'
                if self.grid[x, y] == WALL:
                    color = 'gray'
                elif self.grid[x, y] == FINISH_LINE:
                    color = 'gold'
                elif self.grid[x, y] == OBSTACLE:
                    color = 'red'
                elif self.grid[x, y] == BOOST:
                    color = 'blue'

                ax.add_patch(patches.Rectangle((y, x), 1, 1, color=color))

        # Draw the AI agent
        ax.add_patch(patches.Circle((state.position.y + 0.5, state.position.x + 0.5), 0.3, color='green'))

        ax.set_xlim(0, self.size_y)
        ax.set_ylim(0, self.size_x)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.gca().invert_yaxis()
        plt.show()

    def transition(self, state: State, action: Action):
        """Simulate the agent moving to a new position based on an action."""
        new_x = max(0, min(state.position.x + action.dx, self.size_x - 1))
        new_y = max(0, min(state.position.y + action.dy, self.size_y - 1))

        new_position = Position(new_x, new_y)
        reward = -1  # Penalty for each move
        done = False

        # Check terrain type and adjust accordingly
        terrain = self.grid[new_x, new_y]
        if terrain == OBSTACLE:
            state.damage += 10
            reward -= 20
        elif terrain == BOOST:
            state.speed += 1
            reward += 5
        elif terrain == FINISH_LINE:
            reward += 100
            done = True

        new_state = State(new_position, state.speed, state.fuel - 1, state.damage)
        return new_state, reward, done

    def transition_and_visualize(self, state: State, action: Action):
        """Apply an action, transition to the next state, and visualize it."""
        new_state, reward, done = self.transition(state, action)
        self.visualize_state(new_state)
        return new_state, reward, done

# BFS Search Algorithm
def bfs_search(game: RacingGame):
    queue = deque([(game.initial_state, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        if (current_state.position.x, current_state.position.y) in visited:
            continue

        visited.add((current_state.position.x, current_state.position.y))

        if game.grid[current_state.position.x, current_state.position.y] == FINISH_LINE:
            return path

        # Possible actions (left, right, up, down)
        actions = [Action(0, 1, 0), Action(1, 0, 0), Action(0, -1, 0), Action(-1, 0, 0)]
        for action in actions:
            new_x = current_state.position.x + action.dx
            new_y = current_state.position.y + action.dy
            if 0 <= new_x < game.size_x and 0 <= new_y < game.size_y and (new_x, new_y) not in visited:
                new_position = Position(new_x, new_y)
                new_state = State(new_position, current_state.speed, current_state.fuel, current_state.damage)
                queue.append((new_state, path + [action]))

    return None

def main():
    game = RacingGame(size_x=10, size_y=20)
    path = bfs_search(game)

    if not path:
        print("No path found!")
        return

    current_state = game.initial_state
    total_reward = 0
    game.visualize_state(current_state)

    for action in path:
        current_state, reward, done = game.transition_and_visualize(current_state, action)
        total_reward += reward

        if done:
            print("Reached goal state!")
            break

    print(f"Total reward: {total_reward}")

if __name__ == "__main__":
    main()
