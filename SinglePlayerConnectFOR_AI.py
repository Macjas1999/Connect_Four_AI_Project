import os
from termcolor import colored
import random
import time

from MainConnectFourAI import ConnectFourAI
from Recorder import RecordGamestate
from AnalyzeLayout import AnalyzeLayout
from TrainingDataHandler import TrainingDataHandler

HUMAN_AI_GAMES = "/home/maciej/Desktop/Python/Connect_Four_AI_Project/dataHA/"
ARCHV_DATA = "/home/maciej/Desktop/Python/Connect_Four_AI_Project/dataONW/" 

DATA_PATH = "/home/maciej/Desktop/Python/Connect_Four_AI_Project/dataBuff/"
RESULTS_PATH = "/home/maciej/Desktop/Python/Connect_Four_AI_Project/results/"

RESULTS_EXT_ONE = "resultextract_player_1_vBuff.csv"
RESULTS_EXT_TWO = "resultextract_player_2_vBuff.csv"

MODEL_ONE_SAVED_FILENAME = "model_1_vt3.h5"
MODEL_TWO_SAVED_FILENAME = "model_2_vt3.h5"

MODEL_ONE_NAME = "model_1_vt3"
MODEL_TWO_NAME = "model_2_vt3"

SLEEP_TIME = 0.2

class Board:
    def __init__(self):
        self.ai = ConnectFourAI(MODEL_ONE_SAVED_FILENAME, MODEL_TWO_SAVED_FILENAME)
        self.records = RecordGamestate()
        self.analyzer = AnalyzeLayout()
        self.training_data_handler = TrainingDataHandler(DATA_PATH)


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
            #self.array[i][collumn]

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
        #Main algorythm
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

    def play_ai_player(self, model):
        if self.run: # if one player is not ai you need to specify wchih player it is
            column = self.ai.predict_player(model, self.array)
            #self.add_piece(column, self.player_turn)
            if self.array[0][column-1] != 0:
                self.try_count = 0
                #this is where ai is trying to add piece to full collumn/ need to add some penalty for ai below is temporaary
                while self.array[0][column-1] != 0:
                    column = self.ai.predict_player(model, self.array)
                    #self.analyzer.penalty_for_filling_filled(self.player_turn)
                    if self.try_count > 2:
                        random_input = random.randint(1,7)
                        while self.array[0][random_input-1] != 0:
                            random_input = random.randint(1,7)
                            if self.array[0][random_input-1] == 0:
                                column = random_input
                                self.try_count = 0
                                break
                    self.try_count += 1
            if self.add_piece(column-1, self.player_turn): # if aigen in range 1-7 then -1 is needed to conv to index
                self.analyzer.analyzeBoard(self.array)
                return True
    def play_player(self):
        if self.run:
            try:
                x = input()
                if x == 'e':
                    self.run = False
                    os._exit(0)
                if self.array[0][int(x)-1] != 0:
                    raise Exception("Collumn is full")

                if self.add_piece(int(x)-1, self.player_turn):
                    os.system('tput clear') #displaying only one board
                    self.analyzer.analyzeBoard(self.array)
                    return True
                else:
                    raise Exception("Input is out of range")
            except:
                print('Invalid input')
                x = input('Enter anything to continue')
                os.system('tput clear') #displaying only one board            

    def main_loop(self):
        self.seed = random.randint(100000, 999999)
        self.human_turn = random.randint(1,2)
        while self.run:
            self.draw_board()
            time.sleep(SLEEP_TIME)
            print(f'Player: {self.player_turn}')
            try:
                if self.human_turn == 1:
                    if self.player_turn == 1: 
                        if self.play_player(): #self.play_ai_player(self.ai.model_1)
                            self.look_for_win_move()
                            self.player_turn = 2
                    else:
                        if self.play_ai_player(self.ai.model_2): #self.play_ai_player(self.ai.model_2)
                            self.look_for_win_move()
                            self.player_turn = 1
                elif self.human_turn == 2:
                    if self.player_turn == 1: 
                        if self.play_ai_player(self.ai.model_1): #self.play_ai_player(self.ai.model_1)
                            self.look_for_win_move()
                            self.player_turn = 2
                    else:
                        if self.play_player(): #self.play_ai_player(self.ai.model_2)
                            self.look_for_win_move()
                            self.player_turn = 1
                self.turn_counter += 1
                self.records.snapGamestateEveryturn(999, self.array, self.turn_counter, self.analyzer.playerONEscore, self.analyzer.playerTWOscore, DATA_PATH)
                self.records.snapGamestateEveryturn(self.seed, self.array, self.turn_counter, self.analyzer.playerONEscore, self.analyzer.playerTWOscore, HUMAN_AI_GAMES)
                os.system('tput clear')

            except:
                print('Invalid input')
                #x = input('Enter anything to continue')
                os.system('tput clear')
        #self.records.snapGamestateEveryturn(self.seed, self.array, self.turn_counter, self.analyzer.playerONEscore, self.analyzer.playerTWOscore, DATA_PATH)
        #self.records.snapGamestateEveryturn(self.seed, self.array, self.turn_counter, self.analyzer.playerONEscore, self.analyzer.playerTWOscore, ARCHV_DATA)

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

    app.ai.load_model_v1()

    app.main_loop()
    while True:
        app.training_data_handler.extract_data()
        app.training_data_handler.save_extracted("{0}{1}".format(RESULTS_PATH, RESULTS_EXT_ONE), 1)
        app.training_data_handler.save_extracted("{0}{1}".format(RESULTS_PATH,RESULTS_EXT_TWO), 2)

        app.training_data_handler.load_merged_data("{0}{1}".format(RESULTS_PATH, RESULTS_EXT_ONE))
        app.training_data_handler.load_merged_labels("{0}{1}".format(RESULTS_PATH, RESULTS_EXT_ONE), 1)
        app.training_data_handler.load_merged_labels("{0}{1}".format(RESULTS_PATH,RESULTS_EXT_TWO), 2)

        app.ai.train_player(app.ai.model_1, app.training_data_handler.data, app.training_data_handler.labels_1)
        app.ai.train_player(app.ai.model_2, app.training_data_handler.data, app.training_data_handler.labels_2)
      
        app.ai.save_model_as(MODEL_ONE_NAME, app.ai.model_1)
        app.ai.save_model_as(MODEL_TWO_NAME, app.ai.model_2)  

        app.remove_files(DATA_PATH)
        os.remove("{0}{1}".format(RESULTS_PATH, RESULTS_EXT_ONE))
        os.remove("{0}{1}".format(RESULTS_PATH, RESULTS_EXT_TWO))

        app.reset_game()
        app.analyzer.reset_analyzer()
        app.main_loop()

###
#The whole handling thing is before main loop because player exits game in the main loop            
#so not to loose data it is before this handling stuff
#

#####!
#Costruct system for players to repeat games
#Add a penalty for ai for trying to insert piece to filled up collumn             
#Clean up data/change paths to data folders for this one
#Rebuild data readin and score counting for this one
#
#