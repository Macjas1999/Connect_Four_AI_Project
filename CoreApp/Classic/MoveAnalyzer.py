import copy
from termcolor import colored

from CoreApp.Classic.AnalyzeLayout import AnalyzeLayout, RWARD_WIN
from CoreApp.Classic.Referee import Referee

class MoveAnalyzer:
    INSTANT_WIN_WEIGHT = RWARD_WIN * 10

    def __init__(self):
        self.player_one_weights = [[0] * 7 for _ in range(6)]
        self.player_two_weights = [[0] * 7 for _ in range(6)]

    @staticmethod
    def landing_row(board, column):
        for row in range(5, -1, -1):
            if board[row][column] == 0:
                return row
        return None

    @staticmethod
    def _score_board(board, player):
        analyzer = AnalyzeLayout()
        analyzer.analyzeBoard(board)
        if player == 1:
            return analyzer.playerONEscore - analyzer.playerTWOscore
        return analyzer.playerTWOscore - analyzer.playerONEscore

    @staticmethod
    def _blocks_opponent_win(board, column, player):
        opponent = 2 if player == 1 else 1
        row = MoveAnalyzer.landing_row(board, column)
        if row is None:
            return False

        simulated = copy.deepcopy(board)
        simulated[row][column] = opponent
        return Referee.find_winner(simulated) == opponent

    def _evaluate_move(self, board, column, player):
        row = self.landing_row(board, column)
        if row is None:
            return 0

        simulated = copy.deepcopy(board)
        simulated[row][column] = player

        if Referee.find_winner(simulated) == player:
            return self.INSTANT_WIN_WEIGHT

        weight = self._score_board(simulated, player)
        if self._blocks_opponent_win(board, column, player):
            weight += RWARD_WIN
        return weight

    def analyze(self, board):
        self.player_one_weights = [[0] * 7 for _ in range(6)]
        self.player_two_weights = [[0] * 7 for _ in range(6)]

        for column in range(7):
            row = self.landing_row(board, column)
            if row is None:
                continue

            self.player_one_weights[row][column] = self._evaluate_move(board, column, 1)
            self.player_two_weights[row][column] = self._evaluate_move(board, column, 2)

    def best_move(self, player, board):
        weights = self.player_one_weights if player == 1 else self.player_two_weights
        best_column = None
        best_weight = float('-inf')

        for column in range(7):
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
        if board[row][column] != 0:
            return '   '
        weight = weights[row][column]
        if weight == 0:
            return '   '
        return f'{weight:>3}'

    def _draw_weight_board(self, board, weights, title, color):
        print(colored(title, color, attrs=['bold']))
        for row in range(6):
            print('#|', end='')
            for column in range(7):
                cell = self._format_weight_cell(board, weights, row, column)
                print(colored(cell, color) + '|', end='')
            print('#')
        print('=' * 17)
        print('  ', end='')
        for column in range(7):
            print(f' {column + 1}  ', end='')
        print('\n')

    def draw_maps(self, board):
        self._draw_weight_board(
            board,
            self.player_one_weights,
            'Player 1 (X) move weights',
            'yellow',
        )
        self._draw_weight_board(
            board,
            self.player_two_weights,
            'Player 2 (O) move weights',
            'blue',
        )

        best_p1 = self.best_move(1, board)
        best_p2 = self.best_move(2, board)
        if best_p1 is not None:
            print(f'Best move for P1 (X): column {best_p1 + 1}')
        if best_p2 is not None:
            print(f'Best move for P2 (O): column {best_p2 + 1}')
        print('')
