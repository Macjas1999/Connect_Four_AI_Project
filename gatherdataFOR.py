import os
from termcolor import colored
import csv
import random
import time
from Recorder import RecordedGame
from AnalyzeLayout import AnalyzeLayout

class Board:
    def __init__(self):
        self.array = [[0] * 7 for _ in range(6)]
        self.winning = 0
        self.run = True
        self.player_turn = 1
        clear = lambda : os.system('tput reset')
        clear()
        self.records = RecordedGame()         

    def clear(self):
        lambda : os.system('tput reset')

    def getArray(self):
        for i in range(0,6):
            print(self.array[i])

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
    def look_for_win_move(self, autores):
        #Main algorythm
        self.check_vertical()
        self.check_horizontal()
        self.check_diagonal_b()
        self.check_diagonal_f()
        if self.winning != 0:
            os.system('tput clear')
            self.draw_board()
            if autores:
                print("Winner is Player" + str(self.winning))
                time.sleep(1)
                self.run = False
                return
            else:
                print("Winner is Player" + str(self.winning))
                x = input('Enter anything to exit')
                self.run = False
        else:
            self.check_draw()

    def randomized_input_handling(self, score1, score2):
        x = random.randint(1,7)
        while True:
            if self.add_piece(int(x)-1,self.turn):
                self.look_for_win_move(True)

                if self.turn == 1:
                    self.turn = 2
                    self.player_turn = self.turn
                    self.move += 1
                else:
                    self.turn = 1
                    self.player_turn = self.turn
                    self.move += 1

                break
            else:
                x = random.randint(1,7)
                continue
        
        time.sleep(0.5)
        os.system('tput clear') #displaying only one board
  

    def main_loop(self):
        #
        self.seed = random.randint(100,999)
        analyze = AnalyzeLayout(True) #False-manual input/ True-random automatic input
        self.folder = "/home/maciej/Desktop/Guesser/data1/"
        #
        self.move = 0
        self.turn = 1
        while self.run:
            self.draw_board()

            print(f'Player: {self.turn}')
            #
            analyze.analyzeBoard(self.array)
            print(f'Player 1 score: {analyze.playerONEscore}')
            print(f'Player 2 score: {analyze.playerTWOscore}')

            if analyze.random_input_game:
                self.randomized_input_handling(analyze.playerONEscore, analyze.playerTWOscore)
                analyze.analyzeBoard(self.array)
                self.records.snapGamestateEveryturn(self.seed, self.array, self.move, analyze.playerONEscore, analyze.playerTWOscore, self.folder)


            else:
                try:
                    x = input()
                    if x == 'e':
                        break
                    #
                    # if x == 'i':
                    #     print(self.records)

                    if self.add_piece(int(x)-1,self.turn):
                        self.look_for_win_move(False)
                        #Snappin at last move
                        if self.run == False:
                            self.records.snapGamestateEveryturn(self.seed, self.array, self.turn, analyze.playerONEscore, analyze.playerTWOscore, self.folder)
                        else:
                            #Snapping every move
                            self.records.snapGamestateEveryturn(self.seed, self.array, self.turn, analyze.playerONEscore, analyze.playerTWOscore, self.folder)

                        if self.turn == 1:
                            self.turn = 2
                            self.player_turn = self.turn
                            self.move += 1
                        else:
                            self.turn = 1
                            self.player_turn = self.turn
                            self.move += 1
                    else:
                        raise Exception("Input is out of range")
                    os.system('tput clear') #displaying only one board
                except:
                    print('Invalid input')
                    x = input('Enter anything to continue')
                    os.system('tput clear') #displaying only one board


if __name__ == "__main__":
    #set this loop to define how many simulations to generate
    for i in range(0,50):
        app = Board()
        app.main_loop()

    #app = Board()
    #app.main_loop()

#Need to compile data to trainable set of pairs