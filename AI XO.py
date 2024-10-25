import random

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X goes first (human)
    
    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)
    
    def is_winner(self, player):
        # Check rows, columns, and diagonals
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or \
           all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False
    
    def is_draw(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))

    def get_available_moves(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def undo_move(self, row, col):
        self.board[row][col] = ' '

    def dfs_ai(self):
        # Perform a DFS to find the best move for 'O'
        best_move = None
        for move in self.get_available_moves():
            row, col = move
            self.make_move(row, col, 'O')
            if self.is_winner('O'):
                self.undo_move(row, col)
                return move  # Winning move
            self.undo_move(row, col)
        
        # Block 'X' from winning
        for move in self.get_available_moves():
            row, col = move
            self.make_move(row, col, 'X')
            if self.is_winner('X'):
                self.undo_move(row, col)
                return move  # Block 'X'
            self.undo_move(row, col)

        # Otherwise, pick a random move (DFS-like exploration)
        if not best_move:
            best_move = random.choice(self.get_available_moves())
        
        return best_move

    def play(self):
        while True:
            self.print_board()

            if self.current_player == 'X':  # Human's turn
                row, col = map(int, input("Enter row and column (0-2) for X: ").split())
                if not self.make_move(row, col, 'X'):
                    print("Invalid move. Try again.")
                    continue
            else:  # AI's turn
                row, col = self.dfs_ai()
                self.make_move(row, col, 'O')
                print(f"AI chose position: {row}, {col}")

            if self.is_winner(self.current_player):
                self.print_board()
                print(f"{self.current_player} wins!")
                break

            if self.is_draw():
                self.print_board()
                print("It's a draw!")
                break

            # Switch players
            self.current_player = 'O' if self.current_player == 'X' else 'X'

if __name__ == "__main__":
    game = TicTacToe()
    game.play()
