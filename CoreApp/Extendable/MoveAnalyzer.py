import copy
from termcolor import colored

from Extendable.AnalyzeLayoutExtendable import AnalyzeLayout

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