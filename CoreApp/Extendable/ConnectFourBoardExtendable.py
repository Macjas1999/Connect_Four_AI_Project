import copy
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from termcolor import colored

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from CoreApp.Extendable.Referee import Referee
from CoreApp.Extendable.ConnectFourGUI import ConnectFourGUI
from CoreApp.Extendable.MoveAnalyzer import MoveAnalyzer

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
    print("=== Connect Four - Extended Map (GUI) ===")
    try:
        rows = int(input("Enter number of rows (default 6): ") or "6")
        cols = int(input("Enter number of columns (default 7): ") or "7")

        if rows < 4 or cols < 4:
            print("Board must be at least 4x4 for Connect Four!")
            sys.exit(1)

        app = Board(rows=rows, cols=cols)
        gui = ConnectFourGUI(app)
        gui.root.mainloop()
    except ValueError:
        print("Invalid input!")
        sys.exit(1)

