import os
import numpy as np
from termcolor import colored
import csv
import random
import time
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.utils import to_categorical
from createLearningSet import TrainingDataHandler

class ConnectFourAI:
    def __init__(self):
        self.model_1 = self.build_model_player1()
        self.model_2 = self.build_model_player2()

    def build_model_player1(self):
        model_1 = Sequential()
        model_1.add(Dense(64, input_dim=42, activation='relu'))
        model_1.add(Dense(64, activation='relu'))
        model_1.add(Dense(7, activation='linear'))  # Single output neuron for the score
        model_1.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        return model_1
    
    def build_model_player2(self):
        model_2 = Sequential()
        model_2.add(Dense(64, input_dim=42, activation='relu'))
        model_2.add(Dense(64, activation='relu'))
        model_2.add(Dense(7, activation='linear'))  # Single output neuron for the score
        model_2.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        return model_2

    def board_to_input(self, board):
        return np.array(board).flatten()

    def train_player1(self, X_train, y_train, epochs=100):
        self.model_1.fit(X_train, y_train, epochs=epochs, verbose=0)

    def train_player2(self, X_train, y_train, epochs=100):
        self.model_2.fit(X_train, y_train, epochs=epochs, verbose=0)

    def predict_player1(self, board):
        input_board = self.board_to_input(board)
        prediction = self.model_1.predict(np.array([input_board]))
        return np.argmax(prediction)
    
    def predict_player2(self, board):
        input_board = self.board_to_input(board)
        prediction = self.model_2.predict(np.array([input_board]))
        return np.argmax(prediction)
    
    def save_model_as(self, name, model):
        model.save(''.join(name,'.h5'))

    def load_saved_model_player1(self, name):
        self.model_1 = load_model(name)
    def load_saved_model_player2(self, name):
        self.model_2 = load_model(name)


class RecordedGame:
    def __init__(self) -> None:
        self.recordedGameArray = []

    def recordGamestate(self, array):
        self.recordedGameArray.append(array)

    def snapGamestate(self, seed, array, turn, player):
        stringpath = "{0}{1}{2}{3}{4}{5}{6}".format("/home/maciej/Desktop/Guesser/data/", seed, "t", turn, "p", player, ".csv")
        file = open(stringpath, 'w+', newline ='')
        with file:
            write = csv.writer(file)
            write.writerows(array)

    def snapGamestateWscores(self, seed, array, turn, player, score1, score2):
        stringpath = "{0}{1}{2}{3}{4}{5}{6}".format("/home/maciej/Desktop/Guesser/data/", seed, "t", turn, "p", player, ".csv")
        file = open(stringpath, 'w+', newline ='')
        with file:
            write = csv.writer(file)
            write.writerows(array)
            write.writerow([score1])
            write.writerow([score2])

class Board:
    def __init__(self):
        self.array = [[0] * 7 for _ in range(6)]
        self.winning = 0
        self.run = True
        self.ai = ConnectFourAI()
        self.player_turn = 1
        clear = lambda: os.system('tput reset')
        clear()
        self.records = RecordedGame() 

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


    # Main win-move lookup
    def look_for_win_move(self):
        #Main algorythm
        self.check_vertical()
        self.check_horizontal()
        self.check_diagonal_b()
        self.check_diagonal_f()
        if self.winning != 0:
            os.system('tput clear')
            self.draw_board()
            print("Winner is Player" + str(self.winning))
            x = input('Enter anything to exit')
            self.run = False
            return
        else:
            self.check_draw()

    def play_ai_player1(self):
        if self.player_turn == 1 and self.run:
            column = self.ai.predict_player1(self.array)
            #self.add_piece(column, self.player_turn)
            if self.array[0][column] != 0:
                #this is where ai is trying to add piece to full collumn/ need to add some penalty for ai below is temporaary
                try_count = 0
                while self.array[0][column] != 0:
                    column = self.ai.predict_player1(self.array)
                    try_count += 1
                    if try_count > 50:
                        random_input = random.randint(1,7)
                        while self.array[0][random_input] != 0:
                            random_input = random.randint(1,7)
                            if self.array[0][random_input] == 0:
                                column = random_input
                                break
            if self.add_piece(column-1, self.player_turn): # if aigen in range 1-7 then -1 is needed to conv to index
                return True

    def play_ai_player2(self):
        if self.player_turn == 2 and self.run:
            column = self.ai.predict_player2(self.array)
            #self.add_piece(column, self.player_turn)
            if self.array[0][column] != 0:
                #this is where ai is trying to add piece to full collumn/ need to add some penalty for ai below is temporaary
                try_count = 0
                while self.array[0][column] != 0:
                    column = self.ai.predict_player2(self.array)
                    try_count += 1
                    if try_count > 50:
                        random_input = random.randint(1,7)
                        while self.array[0][random_input] != 0:
                            random_input = random.randint(1,7)
                            if self.array[0][random_input] == 0:
                                column = random_input
                                break

            if self.add_piece(column-1, self.player_turn): # if aigen in range 1-7 then -1 is needed to conv to index
                return True
            
    def main_loop(self):
        while self.run:
            self.draw_board()
            time.sleep(10)
            print(f'Player: {self.player_turn}')
            try:
                if self.player_turn == 1:
                    if self.play_ai_player1():
                        self.look_for_win_move()
                        self.player_turn = 2
                else:
                    if self.play_ai_player2():
                        self.look_for_win_move()
                        self.player_turn = 1

                os.system('tput clear')

            except:
                print('Invalid input')
                x = input('Enter anything to continue')
                os.system('tput clear')

if __name__ == "__main__":
    app = Board()
    datahand = TrainingDataHandler('data1')
    #datahand.extract_data()
    datahand.load_merged_data('resultextract_player1.csv')
    datahand.load_merged_labels('resultextract_player1.csv', 1)
    datahand.load_merged_labels('resultextract_player2.csv', 2)
    #seems i need one-hot vector for ytrain
    #for i in datahand.labels:
    #    i += 200
    #y_train_encoded = to_categorical(datahand.labels, num_classes=7)
    #app.ai.train(datahand.data, y_train_encoded)
    app.ai.train_player1(datahand.data, datahand.labels_1)
    app.ai.train_player2(datahand.data, datahand.labels_2)

    app.main_loop()
