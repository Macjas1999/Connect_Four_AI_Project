import copy
import os
import sys
from pathlib import Path

from termcolor import colored

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from AnalyzeLayoutExtended import AnalyzeLayout


class MoveAnalyzer:
    """Analyzes possible moves for each player and displays weight maps"""
    INSTANT_WIN_WEIGHT = 1920  # RWARD_WIN * 10

    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.player_one_weights = [[0] * cols for _ in range(rows)]
        self.player_two_weights = [[0] * cols for _ in range(rows)]

    def set_board_size(self, rows, cols):
        """Update board size and reinitialize weight matrices"""
        self.rows = rows
        self.cols = cols
        self.player_one_weights = [[0] * cols for _ in range(rows)]
        self.player_two_weights = [[0] * cols for _ in range(rows)]

    @staticmethod
    def landing_row(board, column):
        """Find the row where a piece would land in a column"""
        for row in range(len(board) - 1, -1, -1):
            cell = board[row][column]
            # treat both empty (0) and disabled ('N') cells as not playable
            if cell == 0:
                return row
            elif isinstance(cell, str) and cell.startswith('N'):
                continue
        return None

    @staticmethod
    def _score_board(board, player):
        """Score current board state for a player"""
        analyzer = AnalyzeLayout()
        analyzer.analyzeBoard(board)
        if player == 1:
            return analyzer.playerONEscore - analyzer.playerTWOscore
        return analyzer.playerTWOscore - analyzer.playerONEscore

    @staticmethod
    def _blocks_opponent_win(board, column, player):
        """Check if move blocks opponent from winning"""
        opponent = 2 if player == 1 else 1
        row = MoveAnalyzer.landing_row(board, column)
        if row is None:
            return False

        simulated = copy.deepcopy(board)
        simulated[row][column] = opponent
        
        # check for 4-in-a-row with opponent piece
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        # horizontal
        for c in range(max(0, column - 3), min(cols - 3, column + 1)):
            if all(isinstance(simulated[row][c+d], int) and simulated[row][c+d] == opponent for d in range(4)):
                return True
        # vertical
        for r in range(max(0, row - 3), min(rows - 3, row + 1)):
            if all(isinstance(simulated[r+d][column], int) and simulated[r+d][column] == opponent for d in range(4)):
                return True
        # diagonal down-right
        for offset in range(-3, 1):
            r, c = row + offset, column + offset
            if 0 <= r <= rows - 4 and 0 <= c <= cols - 4:
                if all(isinstance(simulated[r+d][c+d], int) and simulated[r+d][c+d] == opponent for d in range(4)):
                    return True
        # diagonal up-right
        for offset in range(-3, 1):
            r, c = row - offset, column + offset
            if r >= 3 and r < rows and 0 <= c <= cols - 4:
                if all(isinstance(simulated[r-d][c+d], int) and simulated[r-d][c+d] == opponent for d in range(4)):
                    return True
        return False

    def _evaluate_move(self, board, column, player):
        """Evaluate score for a move"""
        row = self.landing_row(board, column)
        if row is None:
            return 0

        simulated = copy.deepcopy(board)
        simulated[row][column] = player

        # check for immediate win
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        # horizontal check
        for c in range(max(0, column - 3), min(cols - 3, column + 1)):
            if all(isinstance(simulated[row][c+d], int) and simulated[row][c+d] == player for d in range(4)):
                return self.INSTANT_WIN_WEIGHT
        # vertical check
        for r in range(max(0, row - 3), min(rows - 3, row + 1)):
            if all(isinstance(simulated[r+d][column], int) and simulated[r+d][column] == player for d in range(4)):
                return self.INSTANT_WIN_WEIGHT
        # diagonal down-right
        for offset in range(-3, 1):
            r, c = row + offset, column + offset
            if 0 <= r <= rows - 4 and 0 <= c <= cols - 4:
                if all(isinstance(simulated[r+d][c+d], int) and simulated[r+d][c+d] == player for d in range(4)):
                    return self.INSTANT_WIN_WEIGHT
        # diagonal up-right
        for offset in range(-3, 1):
            r, c = row - offset, column + offset
            if r >= 3 and r < rows and 0 <= c <= cols - 4:
                if all(isinstance(simulated[r-d][c+d], int) and simulated[r-d][c+d] == player for d in range(4)):
                    return self.INSTANT_WIN_WEIGHT

        weight = self._score_board(simulated, player)
        if self._blocks_opponent_win(board, column, player):
            weight += 192  # RWARD_WIN
        return weight

    def analyze(self, board):
        """Analyze all possible moves for both players"""
        self.player_one_weights = [[0] * self.cols for _ in range(self.rows)]
        self.player_two_weights = [[0] * self.cols for _ in range(self.rows)]

        for column in range(self.cols):
            row = self.landing_row(board, column)
            if row is None:
                continue

            self.player_one_weights[row][column] = self._evaluate_move(board, column, 1)
            self.player_two_weights[row][column] = self._evaluate_move(board, column, 2)

    def best_move(self, player, board):
        """Find best move for player"""
        weights = self.player_one_weights if player == 1 else self.player_two_weights
        best_column = None
        best_weight = float('-inf')

        for column in range(self.cols):
            row = self.landing_row(board, column)
            if row is None:
                continue
            weight = weights[row][column]
            if weight > best_weight:
                best_weight = weight
                best_column = column

        return best_column

    @staticmethod
    def _format_weight_cell(board, weights, row, column):
        """Format a single weight cell for display"""
        cell = board[row][column]
        if cell != 0:
            return '   '
        weight = weights[row][column]
        if weight == 0:
            return '   '
        return f'{weight:>3}'

    def _draw_weight_board(self, board, weights, title, color):
        """Draw a weight map for one player"""
        print(colored(title, color, attrs=['bold']))
        for row in range(self.rows):
            print('#|', end='')
            for column in range(self.cols):
                cell = self._format_weight_cell(board, weights, row, column)
                print(colored(cell, color) + '|', end='')
            print('#')
        print('=' * (self.cols * 2 + 3))
        print('  ', end='')
        for column in range(self.cols):
            print(f'{column + 1} ', end='')
        print('\n')

    def draw_maps(self, board):
        """Display weight maps and best moves for both players"""
        p1_best = self.best_move(1, board)
        p2_best = self.best_move(2, board)
        
        self._draw_weight_board(board, self.player_one_weights, 'Player 1 (X) move weights', 'yellow')
        if p1_best is not None:
            print(colored(f'Player 1 best move: Column {p1_best + 1}', 'yellow', attrs=['bold']))
        print()
        
        self._draw_weight_board(board, self.player_two_weights, 'Player 2 (O) move weights', 'blue')
        if p2_best is not None:
            print(colored(f'Player 2 best move: Column {p2_best + 1}', 'blue', attrs=['bold']))
        print()


class Referee:
    @staticmethod
    def find_all_connect_fours(board):
        """Find all connect-four positions and return list of (player, start_pos, direction)"""
        connects = []
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        for row in range(rows - 3):
            for col in range(cols):
                if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'vertical'))
        
        for row in range(rows):
            for col in range(cols - 3):
                if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'horizontal'))
        
        for row in range(rows - 3):
            for col in range(cols - 3):
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'diag_f'))
        
        for row in range(3, rows):
            for col in range(cols - 3):
                if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'diag_b'))
        
        return connects

    @staticmethod
    def check_draw(board):
        return all(all(cell != 0 for cell in row) for row in board)

    @staticmethod
    def find_and_mark_connect_fours(board):
        """Scan left-to-right, top-to-bottom. When a connect-four is found,
        immediately mark its four cells as disabled ('N1'/'N2') so they
        won't be counted again. Returns (p1_count, p2_count)."""
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        p1 = 0
        p2 = 0

        for row in range(rows):
            for col in range(cols):
                cell = board[row][col]
                # only integer pieces can start a new connect
                if not isinstance(cell, int) or cell == 0:
                    continue
                player = cell

                # check horizontal (left-to-right)
                if col + 3 < cols:
                    coords = [(row, col + d) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

                # check vertical (top-to-bottom)
                if row + 3 < rows:
                    coords = [(row + d, col) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

                # check diagonal down-right
                if row + 3 < rows and col + 3 < cols:
                    coords = [(row + d, col + d) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

                # check diagonal up-right
                if row - 3 >= 0 and col + 3 < cols:
                    coords = [(row - d, col + d) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

        return p1, p2


class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.array = [[0] * cols for _ in range(rows)]
        self.run = True
        self.player_turn = 1
        self.move_analyzer = MoveAnalyzer(rows, cols)
        self.player_one_wins = 0
        self.player_two_wins = 0
        self.clear()

    def clear(self):
        os.system('tput reset')

    def getArray(self):
        for i in range(self.rows):
            print(self.array[i])

    def draw_board(self):
        self.clear()
        for i in range(self.rows):
            print('#|', end='')
            for j in range(self.cols):
                cell = self.array[i][j]
                # treat disabled "N" cells (strings like 'N1','N2') specially
                if cell == 0:
                    print(' |', end='')
                elif cell == 1:
                    print(colored('X', 'yellow', attrs=['bold']) + '|', end='')
                elif cell == 2:
                    print(colored('O', 'blue', attrs=['bold']) + '|', end='')
                elif isinstance(cell, str) and cell.startswith('N'):
                    # color N according to owning player
                    owner = cell[1:]
                    if owner == '1':
                        print(colored('X', 'red', attrs=['bold']) + '|', end='')
                    elif owner == '2':
                        print(colored('O', 'red', attrs=['bold']) + '|', end='')
                    else:
                        print(colored('N', 'white', attrs=['bold']) + '|', end='')
            print('#', end='\n')
        for i in range(self.cols * 2 + 3):
            print('=', end='')
        print('')
        print('  ', end='')
        for j in range(self.cols):
            print(f'{j + 1} ', end='')
        print('\n')

    def add_piece(self, column, player):
        for i in range(self.rows - 1, -1, -1):
            if self.array[i][column] == 0:
                self.array[i][column] = player
                return True
        return False

    def check_for_connects(self):
        """Check for all connect-fours and return counts"""
        connects = Referee.find_all_connect_fours(self.array)
        player_one_count = sum(1 for p, _, _ in connects if p == 1)
        player_two_count = sum(1 for p, _, _ in connects if p == 2)
        return player_one_count, player_two_count

    def handle_connect_fours(self):
        """Process connect-fours found on board, update counts"""
        p1_count, p2_count = Referee.find_and_mark_connect_fours(self.array)
        if p1_count > 0:
            self.player_one_wins += p1_count
            print(f"Player 1 connected! +{p1_count}  Total: {self.player_one_wins}")
        if p2_count > 0:
            self.player_two_wins += p2_count
            print(f"Player 2 connected! +{p2_count}  Total: {self.player_two_wins}")

    def check_board_state(self):
        """Check if board is full (draw)"""
        if Referee.check_draw(self.array):
            print(f"\nBoard is full! Game Over!")
            print(f"Final Scores - Player 1: {self.player_one_wins}, Player 2: {self.player_two_wins}")
            self.run = False

    def main_loop(self):
        turn = 1
        move_count = 0
        while self.run:
            self.draw_board()
            
            # Analyze and display move weights
            self.move_analyzer.analyze(self.array)
            self.move_analyzer.draw_maps(self.array)
            
            print(f'Player: {turn}')
            print(f'Scores - P1: {self.player_one_wins} | P2: {self.player_two_wins}')
            print(f'Move: {move_count}')
            print("(Enter column 1-{}, or 'e' to exit)".format(self.cols))
            
            try:
                x = input()
                if x == 'e':
                    self.run = False
                    break

                column = int(x) - 1
                if column < 0 or column >= self.cols:
                    raise ValueError(f"Column out of range (1-{self.cols})")

                if self.add_piece(column, turn):
                    self.handle_connect_fours()
                    self.check_board_state()
                    
                    if self.run:
                        turn = 2 if turn == 1 else 1
                        move_count += 1
                else:
                    raise ValueError("Column is full")
            except ValueError as e:
                print(f'Invalid input: {e}')
                input('Enter anything to continue')



if __name__ == "__main__":
    print("=== Connect Four - Extended Map ===")
    try:
        rows = int(input("Enter number of rows (default 6): ") or "6")
        cols = int(input("Enter number of columns (default 7): ") or "7")
        
        if rows < 4 or cols < 4:
            print("Board must be at least 4x4 for Connect Four!")
            sys.exit(1)
            
        app = Board(rows=rows, cols=cols)
        app.main_loop()
    except ValueError:
        print("Invalid input!")
        sys.exit(1)

