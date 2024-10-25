import random
import sys

# Directions: (dx, dy) for up, down, left, right
DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

class SnakeGame:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.snake = [(height // 2, width // 2)]  # Start snake in center
        self.food = self.generate_food()
        self.direction = 'UP'

    def generate_food(self):
        while True:
            food = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
            if food not in self.snake:
                return food

    def is_valid(self, position):
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width and position not in self.snake

    def dfs_search(self, target):
        # DFS to find the path to food
        stack = [(self.snake[0], [])]  # Start with the head of the snake
        visited = set()

        while stack:
            position, path = stack.pop()
            if position == target:
                return path  # Return path to the food

            if position in visited:
                continue

            visited.add(position)

            for direction, (dx, dy) in DIRECTIONS.items():
                new_pos = (position[0] + dx, position[1] + dy)
                if self.is_valid(new_pos):
                    stack.append((new_pos, path + [direction]))

        return []  

    def move_snake(self, direction):
        dx, dy = DIRECTIONS[direction]
        new_head = (self.snake[0][0] + dx, self.snake[0][1] + dy)

        if not self.is_valid(new_head):
            print("Game Over!")
            sys.exit()

        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food:
            self.snake.append(self.snake[-1])  
            self.food = self.generate_food()  

    def play(self):
        while True:
            path = self.dfs_search(self.food)
            if path:
                for move in path:
                    self.move_snake(move)
                    self.print_board()
            else:
                print("No path to food. Game Over!")
                break

    def print_board(self):
        board = [['.' for _ in range(self.width)] for _ in range(self.height)]

        for x, y in self.snake:
            board[x][y] = 'S'
        food_x, food_y = self.food
        board[food_x][food_y] = 'F'

        print("\n".join(" ".join(row) for row in board))
        print("\n")

if __name__ == "__main__":
    game = SnakeGame()
    game.play()
