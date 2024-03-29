import os
from termcolor import colored
import random
import time
import numpy as np

from MainConnectFourAI import ConnectFourAI
from Recorder import RecordGamestate
from AnalyzeLayout import AnalyzeLayout
from TrainingDataHandler import TrainingDataHandler

DATA_PATH = "/home/maciej/Desktop/Python/Connect_Four_AI_Project/data/"

MODEL_ONE_SAVED_FILENAME = "model_1_v10.h5"
MODEL_TWO_SAVED_FILENAME = "model_2_v10.h5"

MODEL_ONE_NAME = "model_1_v10"
MODEL_TWO_NAME = "model_2_v10"

SLEEP_TIME = 0.05

class Board:
    def __init__(self):
        self.ai = ConnectFourAI(MODEL_ONE_SAVED_FILENAME, MODEL_TWO_SAVED_FILENAME)
        self.records = RecordGamestate()
        self.analyzer = AnalyzeLayout()

        self.array = [[0] * 7 for _ in range(6)]
        self.winning = 0
        self.run = True
        self.turn_counter = 0
        self.player_turn = 1
        clear = lambda: os.system('tput reset')
        clear()
        self.try_count = 0

    def reset_game(self):
        self.array = [[0] * 7 for _ in range(6)]
        self.winning = 0
        self.run = True
        self.turn_counter = 0
        self.player_turn = 1
        clear = lambda: os.system('tput reset')
        clear()

    def clear(self):
        lambda : os.system('tput reset')

    def draw_board(self):
        self.clear()
        for i in range(0,6):
            print('#|', end='')
            for j in range(0,7):
                match self.array[i][j]:
                    case 0:
                        print(' |', end='') 
                    case 1:
                        print(colored('O', 'yellow', attrs=['bold'])+'|', end='')
                    case 2:
                        print(colored('O', 'blue', attrs=['bold'])+'|', end='')         
                #print(f'{self.array[i][j]}|', end='')
            print('#', end='\n')
        for i in range(0,17):
            print('=', end='')
        print('')
        print('  ', end='')
        for j in range(0,7):
            print(f'{j+1} ', end='')
        print('\n')

    def add_piece(self, collumn, player):
        for i in range(5,-1,-1):
            if self.array[i][collumn] == 0:
                self.array[i][collumn] = player
                return True
            else:
                if i == 0:
                    return False
                else:
                    continue

##############################
### Veryfication
    def check_vertical(self):
        for i in range(0, 3):
            for j in range(0, 7):
                if self.array[i][j] == self.array[i+1][j] == self.array[i+2][j] == self.array[i+3][j]:
                    if self.array[i][j] != 0:
                        self.winning = self.array[i][j]

    def check_horizontal(self):
        for i in range(0, 6):
            for j in range(0, 4):
                if self.array[i][j] == self.array[i][j+1] == self.array[i][j+2] == self.array[i][j+3]:
                    if self.array[i][j] != 0:
                        self.winning = self.array[i][j]


    def check_diagonal_f(self):
        for i in range(0,3):
            for j in range(0,4):
                if self.array[i][j] == self.array[i+1][j+1] == self.array[i+2][j+2] == self.array[i+3][j+3]:
                    if self.array[i][j] != 0:
                        self.winning = self.array[i][j]


    def check_diagonal_b(self):
        for i in range(3,6):
            for j in range(0,4):
                if self.array[i][j] == self.array[i-1][j+1] == self.array[i-2][j+2] == self.array[i-3][j+3]:
                    if self.array[i][j] != 0:
                        self.winning = self.array[i][j]


    def check_draw(self):
        if all(all(cell != 0 for cell in row) for row in self.array):
            print("It's a draw!")
            self.run = False
            

    def look_for_win_move(self):
        self.check_vertical()
        self.check_horizontal()
        self.check_diagonal_b()
        self.check_diagonal_f()
        if self.winning != 0:
            os.system('tput clear')
            self.draw_board()
            self.run = False
            return
        else:
            self.check_draw()

##############################
### Moves
    def play_ai_player(self, model):
        if self.run: 
            collumn = self.ai.make_move(model, self.array)
            if self.add_piece(collumn, self.player_turn): # if aigen in range 1-7 then -1 is needed to conv to index
                self.analyzer.analyzeBoard(self.array)
                return collumn
            
    def play_human_player(self):
        if self.run:
            while True:
                try:
                    collumn = input()
                    if collumn == 'e':
                        self.run = False
                        os._exit(0)
                    if self.array[0][int(collumn)-1] != 0:
                        raise Exception("Collumn is full")

                    elif self.add_piece(int(collumn)-1, self.player_turn):
                        self.analyzer.analyzeBoard(self.array)
                        os.system('tput clear') #displaying only one board
                        return collumn
                    else:
                        raise Exception("Input is out of range")
                except:
                    print('Invalid input')
                    collumn = input('Enter anything to continue')
                    os.system('tput clear') #displaying only one board   
                    self.draw_board()


##############################
### Game main loop conigurations
    def main_loop_HvH(self, game_num): # Human versus human
        self.seed = random.randint(1000, 9999)
        while self.run:
            self.draw_board()
            time.sleep(SLEEP_TIME)
            print(f'Player: {self.player_turn}')
            print(f'Game: {game_num}')
            try:
                if self.player_turn == 1:
                    move = self.play_human_player()
                    self.look_for_win_move()
                    self.player_turn = 2
                else:
                    move = self.play_human_player()
                    self.look_for_win_move()
                    self.player_turn = 1

                self.turn_counter += 1
                ###Recording
                self.records.snapGamestateEveryturn(self.seed, self.array, self.turn_counter, move, self.analyzer.playerONEscore, self.analyzer.playerTWOscore, DATA_PATH)
                os.system('tput clear')

            except:
                print('Invalid input')
                #x = input('Enter anything to continue')
                os.system('tput clear')

    def main_loop_HvAI(self, game_num): # Human versus AI
        self.seed = random.randint(1000, 9999)
        self.human_turn = random.randint(1,2)
        while self.run:
            self.draw_board()
            time.sleep(SLEEP_TIME)
            print(f'Player: {self.player_turn}')
            print(f'Game: {game_num}')
            try:
                if self.human_turn == 1:
                    if self.player_turn == 1: 
                        move = self.play_human_player()
                        self.look_for_win_move()
                        self.player_turn = 2
                    else:
                        move = self.play_ai_player(self.ai.model_2)
                        self.look_for_win_move()
                        self.player_turn = 1

                elif self.human_turn == 2:
                    if self.player_turn == 1: 
                        move = self.play_ai_player(self.ai.model_1)
                        self.look_for_win_move()
                        self.player_turn = 2
                    else:
                        move = self.play_human_player()
                        self.look_for_win_move()
                        self.player_turn = 1

                self.turn_counter += 1
                self.records.snapGamestateEveryturn(self.seed, self.array, self.turn_counter, move, self.analyzer.playerONEscore, self.analyzer.playerTWOscore, DATA_PATH)
                os.system('tput clear')

            except:
                print('Invalid input')
                #x = input('Enter anything to continue')
                os.system('tput clear')

    def main_loop_AIvAI(self, game_num): # AI versus AI
        self.seed = random.randint(1000, 9999)
        while self.run:
            self.draw_board()
            time.sleep(SLEEP_TIME)
            print(f'Player: {self.player_turn}')
            print(f'Game: {game_num}')
            try:
                if self.player_turn == 1:
                    move = self.play_ai_player(self.ai.model_1)
                    self.look_for_win_move()
                    self.player_turn = 2
                else:
                    move = self.play_ai_player(self.ai.model_2)
                    self.look_for_win_move()
                    self.player_turn = 1

                self.turn_counter += 1
                ###Recording
                self.records.snapGamestateEveryturn(self.seed, self.array, self.turn_counter, move, self.analyzer.playerONEscore, self.analyzer.playerTWOscore, DATA_PATH)
                os.system('tput clear')

            except:
                print('Invalid input')
                #x = input('Enter anything to continue')
                os.system('tput clear')

##############################
### Misc
    def remove_files(self, directory):
        for filename in os.listdir(directory):
            file_path = "{0}{1}".format(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                
            except Exception as e:
                print("Error removing")

    
if __name__ == "__main__":
    app = Board()

    app.ai.train_player_v2(DATA_PATH)
    app.main_loop_HvAI(0)
    for i in range(1,4):
        app.reset_game()
        app.main_loop_HvAI(i)
