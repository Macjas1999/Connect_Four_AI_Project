import copy
import os
import sys
import time
from pathlib import Path
from termcolor import colored

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Classic.AnalyzeLayout import AnalyzeLayout, RWARD_WIN
from Classic.Referee import Referee
from Classic.MoveAnalyzer import MoveAnalyzer


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

### Main loops for the game
    def main_loop_dev_mode(self):
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

    def main_loop_pvp(self):
        turn = 1
        while self.run:
            self.draw_board()

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

    def main_loop_ai(self, user_choice):
        turn = 1
        if user_choice == 1:
            self.ai_player = 2
            self.human_player = 1
        else:
            self.ai_player = 1
            self.human_player = 2

        while self.run:
            self.draw_board()
            self.move_analyzer.analyze(self.array)
            #self.move_analyzer.draw_maps(self.array)

            print(f'Player: {turn}')
            if turn == self.human_player:
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
            else:
                print('AI is thinking...')
                time.sleep(1) # Simulate thinking time
                column = self.move_analyzer.best_move(self.ai_player, self.array)
                if self.add_piece(column, turn):
                    self.look_for_win_move()
                    if turn == 1:
                        turn = 2
                        self.player_turn = turn
                    else:
                        turn = 1
                        self.player_turn = turn
                else:
                    print('AI made an invalid move')
                    input('Enter anything to continue')
                    os.system('tput clear')

if __name__ == "__main__":
    app = Board()
    print('Welcome to Connect Four! \n' \
    'Input "1" for Player vs Player \n' \
    'Input "2" for Player vs AI \n' \
    'Input "3" for dev mode \n' \
    'Input "e" to exit')
    try:
        x = input(': ')
        
        os.system('tput clear')
        if x == 'e':
            sys.exit()

        elif x == '1':
            app.main_loop_pvp()

        elif x == '2':
            y = input('Play as Player 1 or Player 2? (Input "1" or "2"): ')
            os.system('tput clear')
            if y == '1':
                app.main_loop_ai(1)
            elif y == '2':
                app.main_loop_ai(2)
            else:
                print('Invalid input')
                input('Enter anything to continue')
                os.system('tput clear')

        elif x == '3':
            app.main_loop_dev_mode()

    except ValueError:
        print('Invalid input')
        input('Enter anything to continue')
        os.system('tput clear')
