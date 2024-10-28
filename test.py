from enum import Enum
import numpy as np
import time
import os
from typing import List

class TerrainSymbol:
    ROAD = '.'      # Normal road
    BOOST = '>'     # Speed boost
    OBSTACLE = 'X'  # Obstacle
    RECHARGE = 'F'  # Fuel station
    WALL = '#'      # Wall
    FINISH = 'G'    # Goal/Finish line
    AGENT = 'A'     # Agent/Car

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class RacingGameVisualizer:
    def __init__(self, size_x: int = 10, size_y: int = 20):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = np.zeros((size_x, size_y), dtype=int)
        self._initialize_track()
        
        # Initial position
        self.agent_pos = [size_x // 2, 0]
        
    def _initialize_track(self):
        """Initialize track with terrain"""
        # Set roads
        self.grid.fill(0)
        
        # Set walls
        self.grid[0, :] = 4
        self.grid[-1, :] = 4
        
        # Set finish line
        self.grid[1:-1, -1] = 5
        
        # Add obstacles in a pattern to make it interesting
        # Create two diagonal lines of obstacles
        for i in range(1, self.size_x-1):
            y = (i * 2) % (self.size_y-2)
            if y < self.size_y-2:
                self.grid[i, y] = 2
        
        # Add boost pads before obstacles
        for i in range(1, self.size_x-1):
            for j in range(1, self.size_y-1):
                if self.grid[i, j] == 0 and j < self.size_y-2:
                    if [i-1, j+1] in [[x, y] for x, y in zip(*np.where(self.grid == 2))]:
                        self.grid[i, j] = 1
        
        # Add recharge stations
        self.grid[1, self.size_y//2] = 3
        self.grid[self.size_x-2, self.size_y//2] = 3

    def get_symbol(self, value: int) -> str:
        symbols = {
            0: TerrainSymbol.ROAD,
            1: TerrainSymbol.BOOST,
            2: TerrainSymbol.OBSTACLE,
            3: TerrainSymbol.RECHARGE,
            4: TerrainSymbol.WALL,
            5: TerrainSymbol.FINISH
        }
        return symbols.get(value, '?')

    def display_game(self, agent_pos=None):
        """Display the current game state"""
        if agent_pos is None:
            agent_pos = self.agent_pos
            
        clear_console()
        
        # Print column numbers
        print("   ", end="")
        for j in range(self.size_y):
            print(f"{j%10}", end=" ")
        print("\n")
        
        # Print grid with agent
        for i in range(self.size_x):
            # Print row numbers
            print(f"{i:2} ", end="")
            
            for j in range(self.size_y):
                if [i, j] == agent_pos:
                    print(TerrainSymbol.AGENT, end=" ")
                else:
                    print(self.get_symbol(self.grid[i, j]), end=" ")
            
            # Print legend for this row
            if i == 0:
                print("   Legend:")
            elif i == 1:
                print(f"   {TerrainSymbol.AGENT} = Agent/Car")
            elif i == 2:
                print(f"   {TerrainSymbol.ROAD} = Road")
            elif i == 3:
                print(f"   {TerrainSymbol.BOOST} = Speed Boost")
            elif i == 4:
                print(f"   {TerrainSymbol.OBSTACLE} = Obstacle")
            elif i == 5:
                print(f"   {TerrainSymbol.RECHARGE} = Fuel Station")
            elif i == 6:
                print(f"   {TerrainSymbol.WALL} = Wall")
            elif i == 7:
                print(f"   {TerrainSymbol.FINISH} = Finish Line")
            else:
                print()
            
        print()

    def animate_path(self, path: List[List[int]], delay: float = 0.5):
        """Animate the agent following a path"""
        for pos in path:
            self.display_game(pos)
            time.sleep(delay)

def main():
    # Create and display initial game state
    game = RacingGameVisualizer(10, 20)
    game.display_game()
    
    # Example path (you would replace this with BFS path)
    example_path = [
        [5, 0],  # Start
        [5, 1],
        [4, 2],
        [4, 3],
        [5, 4],
        [5, 5],
        [6, 6],
        [5, 7],
        [4, 8],
        [4, 9],
        [5, 10],
        [5, 11],
        [4, 12],
        [4, 13],
        [5, 14],
        [5, 15],
        [4, 16],
        [4, 17],
        [4, 18],
        [4, 19]   # Finish
    ]
    
    input("\nPress Enter to start animation...")
    game.animate_path(example_path)

if __name__ == "__main__":
    main()