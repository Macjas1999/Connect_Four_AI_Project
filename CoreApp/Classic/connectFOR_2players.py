import copy
import os
import sys
from pathlib import Path

from termcolor import colored

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from CoreApp.Classic.AnalyzeLayout import AnalyzeLayout, RWARD_WIN


class Referee:
    @staticmethod
    def check_vertical(board):
        for i in range(0, 3):
            for j in range(0, 7):
                if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_horizontal(board):
        for i in range(0, 6):
            for j in range(0, 4):
                if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_diagonal_f(board):
        for i in range(0, 3):
            for j in range(0, 4):
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_diagonal_b(board):
        for i in range(3, 6):
            for j in range(0, 4):
                if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_draw(board):
        return all(all(cell != 0 for cell in row) for row in board)

    @staticmethod
    def find_winner(board):
        for check in (
            Referee.check_vertical,
            Referee.check_horizontal,
            Referee.check_diagonal_b,
            Referee.check_diagonal_f,
        ):
            winner = check(board)
            if winner != 0:
                return winner
        return 0


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


class Board:
    def __init__(self):
        self.array = [[0] * 7 for _ in range(6)]
        self.winning = 0
        self.run = True
        self.player_turn = 1
        self.move_analyzer = MoveAnalyzer()
        self.clear()

    def clear(self):
        os.system('tput reset')

    def getArray(self):
        for i in range(0, 6):
            print(self.array[i])

    def draw_board(self):
        self.clear()
        for i in range(0, 6):
            print('#|', end='')
            for j in range(0, 7):
                match self.array[i][j]:
                    case 0:
                        print(' |', end='')
                    case 1:
                        print(colored('X', 'yellow', attrs=['bold']) + '|', end='')
                    case 2:
                        print(colored('O', 'blue', attrs=['bold']) + '|', end='')
            print('#', end='\n')
        for i in range(0, 17):
            print('=', end='')
        print('')
        print('  ', end='')
        for j in range(0, 7):
            print(f'{j + 1} ', end='')
        print('\n')

    def add_piece(self, collumn, player):
        for i in range(5, -1, -1):
            if self.array[i][collumn] == 0:
                self.array[i][collumn] = player
                return True
            else:
                if i == 0:
                    return False
                else:
                    continue

    def look_for_win_move(self):
        self.winning = Referee.find_winner(self.array)
        if self.winning != 0:
            os.system('tput clear')
            self.draw_board()
            print("Winner is Player" + str(self.winning))
            input('Enter anything to exit')
            self.run = False
            return

        if Referee.check_draw(self.array):
            print("It's a draw!")
            self.run = False

    def main_loop(self):
        turn = 1
        while self.run:
            self.draw_board()
            self.move_analyzer.analyze(self.array)
            self.move_analyzer.draw_maps(self.array)

            print(f'Player: {turn}')
            try:
                x = input()
                if x == 'e':
                    self.run = False
                    break

                column = int(x) - 1
                if column < 0 or column > 6:
                    raise ValueError("Column out of range")

                if self.add_piece(column, turn):
                    self.look_for_win_move()
                    if turn == 1:
                        turn = 2
                        self.player_turn = turn
                    else:
                        turn = 1
                        self.player_turn = turn
                else:
                    raise ValueError("Column is full")
                os.system('tput clear')
            except ValueError:
                print('Invalid input')
                input('Enter anything to continue')
                os.system('tput clear')


if __name__ == "__main__":
    app = Board()
    app.main_loop()
