REWARD_ONE = 1
REWARD_TWO = 4
REWARD_THREE = 16
RWARD_WIN = 192
PENALTY_FILLED_UP_TRY = 32 

class AnalyzeLayout:
    def __init__(self):
        self.playerONEscore = 0
        self.playerTWOscore = 0
        #self.random_input_game = use_rand

        # self.playerONE_fill_miss = 0
        # self.playerTWO_fill_miss = 0


    def analyzeBoard(self, array):
        self.playerONEscore = 0
        self.playerTWOscore = 0
        self.c1_all(array)
        self.c4_vertical(array)
        self.c4_horizontal(array)
        self.c4_diagonal_f(array)
        self.c4_diagonal_b(array)
        self.c3_horizontal(array)
        self.c3_vertical(array)
        self.c3_diagonal_f(array)
        self.c3_diagonal_b(array)
        self.c2_horizontal(array)
        self.c2_vertical(array)
        self.c2_diagonal_f(array)
        self.c2_diagonal_b(array)

        # self.playerONEscore -= self.playerONE_fill_miss
        # self.playerTWOscore -= self.playerTWO_fill_miss

        self.check_draw_reward(array)
        
    def reset_analyzer(self):
        self.playerONEscore = 0
        self.playerTWOscore = 0
        #self.random_input_game = use_rand

        # self.playerONE_fill_miss = 0
        # self.playerTWO_fill_miss = 0

    def c1_all(self, array):
        for i in range(0,6):
            for j in range(0,7):
                match array[i][j]:
                    case 0:
                        pass
                    case 1:
                        self.playerONEscore += REWARD_ONE
                    case 2:
                        self.playerTWOscore += REWARD_ONE


    #3 in row
    def c3_vertical(self, array):
        for i in range(0, 4):
            for j in range(0, 7):
                if array[i][j] == array[i+1][j] == array[i+2][j]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_THREE
                        else:
                            self.playerTWOscore += REWARD_THREE                

    def c3_horizontal(self, array):
        for i in range(0, 6):
            for j in range(0, 5):
                if array[i][j] == array[i][j+1] == array[i][j+2]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_THREE
                        else:
                            self.playerTWOscore += REWARD_THREE


    def c3_diagonal_f(self, array):
        for i in range(0,4):
            for j in range(0,5):
                if array[i][j] == array[i+1][j+1] == array[i+2][j+2]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_THREE
                        else:
                            self.playerTWOscore += REWARD_THREE


    def c3_diagonal_b(self, array):
        for i in range(2,6):
            for j in range(0,5):
                if array[i][j] == array[i-1][j+1] == array[i-2][j+2]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_THREE
                        else:
                            self.playerTWOscore += REWARD_THREE
    #2 in row
    def c2_vertical(self, array):
        for i in range(0, 5):
            for j in range(0, 7):
                if array[i][j] == array[i+1][j]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_TWO
                        else:
                            self.playerTWOscore += REWARD_TWO
                        

    def c2_horizontal(self, array):
        for i in range(0, 6):
            for j in range(0, 6):
                if array[i][j] == array[i][j+1]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_TWO
                        else:
                            self.playerTWOscore += REWARD_TWO


    def c2_diagonal_f(self, array):
        for i in range(0,5):
            for j in range(0,6):
                if array[i][j] == array[i+1][j+1]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_TWO
                        else:
                            self.playerTWOscore += REWARD_TWO


    def c2_diagonal_b(self, array):
        for i in range(1,6):
            for j in range(0,6):
                if array[i][j] == array[i-1][j+1]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += REWARD_TWO
                        else:
                            self.playerTWOscore += REWARD_TWO

    def c4_vertical(self, array):
        for i in range(0, 3):
            for j in range(0, 7):
                if array[i][j] == array[i+1][j] == array[i+2][j] == array[i+3][j]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += RWARD_WIN
                        else:
                            self.playerTWOscore += RWARD_WIN

    def c4_horizontal(self, array):
        for i in range(0, 6):
            for j in range(0, 4):
                if array[i][j] == array[i][j+1] == array[i][j+2] == array[i][j+3]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += RWARD_WIN
                        else:
                            self.playerTWOscore += RWARD_WIN


    def c4_diagonal_f(self, array):
        for i in range(0,3):
            for j in range(0,4):
                if array[i][j] == array[i+1][j+1] == array[i+2][j+2] == array[i+3][j+3]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += RWARD_WIN
                        else:
                            self.playerTWOscore += RWARD_WIN


    def c4_diagonal_b(self, array):
        for i in range(3,6):
            for j in range(0,4):
                if array[i][j] == array[i-1][j+1] == array[i-2][j+2] == array[i-3][j+3]:
                    if array[i][j] != 0:
                        if array[i][j] == 1:
                            self.playerONEscore += RWARD_WIN
                        else:
                            self.playerTWOscore += RWARD_WIN

    # def penalty_for_filling_filled(self, player):
    #     if player == 1:
    #         self.playerONE_fill_miss += PENALTY_FILLED_UP_TRY
    #     elif player == 2:
    #         self.playerTWO_fill_miss += PENALTY_FILLED_UP_TRY
    #     else:
    #         pass

    def check_draw_reward(self, array):
        if all(all(cell != 0 for cell in row) for row in array):
            self.playerONEscore = 0
            self.playerTWOscore = 0

#Winning analisys
    def run_win_check(self, array):
        if self.check_vertical(array) != 0:
            return self.check_vertical(array)
        elif self.check_horizontal(array) != 0:
            return self.check_horizontal(array)
        elif self.check_diagonal_f(array) != 0:
            return self.check_diagonal_f(array)
        elif self.check_diagonal_b(array) != 0:
            return self.check_diagonal_b(array)
        elif self.check_draw(array) == 3:
            return 3


    def check_vertical(self, array):
        for i in range(0, 3):
            for j in range(0, 7):
                if array[i][j] == array[i+1][j] == array[i+2][j] == array[i+3][j]:
                    if array[i][j] != 0:
                        return array[i][j]
        return 0

    def check_horizontal(self, array):
        for i in range(0, 6):
            for j in range(0, 4):
                if array[i][j] == array[i][j+1] == array[i][j+2] == array[i][j+3]:
                    if array[i][j] != 0:
                        return array[i][j]
        return 0


    def check_diagonal_f(self, array):
        for i in range(0,3):
            for j in range(0,4):
                if array[i][j] == array[i+1][j+1] == array[i+2][j+2] == array[i+3][j+3]:
                    if array[i][j] != 0:
                        return array[i][j]
        return 0


    def check_diagonal_b(self, array):
        for i in range(3,6):
            for j in range(0,4):
                if array[i][j] == array[i-1][j+1] == array[i-2][j+2] == array[i-3][j+3]:
                    if array[i][j] != 0:
                        return array[i][j]
        return 0

    def check_draw(self, array):
        if all(all(cell != 0 for cell in row) for row in array):
            return 3