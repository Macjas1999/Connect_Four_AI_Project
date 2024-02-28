import os
from termcolor import colored

class Board:
    def __init__(self):
        self.array = [[0] * 7 for _ in range(6)]
        self.winning = 0
        self.run = True
        self.player_turn = 1
        clear = lambda : os.system('tput reset')
        clear()

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
    def look_for_win_move(self):
        #Recording
        self.records.recordGamestate(self.array, self.player_turn)
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


    def main_loop(self):
        turn = 1
        while self.run:
            self.draw_board()

            print(f'Player: {turn}')
            try:
                x = input()
                if x == 'e':
                    break

                if self.add_piece(int(x)-1,turn):
                    self.look_for_win_move()
                    if turn == 1:
                        turn = 2
                        self.player_turn = turn
                    else:
                        turn = 1
                        self.player_turn = turn
                else:
                    raise Exception("Input is out of range")
                os.system('tput clear') #displaying only one board
            except:
                print('Invalid input')
                x = input('Enter anything to continue')
                os.system('tput clear') #displaying only one board

if __name__ == "__main__":
    app = Board()
    app.main_loop()
