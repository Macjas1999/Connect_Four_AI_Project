import os
import pandas as pd
import numpy as np
import re

class TrainingDataHandler:

    def __init__(self, dir):
        self.directory = dir
        self.list_of_datafiles = []
        for filename in os.listdir(self.directory):
            if filename.endswith(".csv"):
                self.list_of_datafiles.append(os.path.join(self.directory, filename))


    def handler_get_state(self, filename):
        df = pd.read_csv(filename, index_col=None, header=None)
        #self.data = np.array(df.values).reshape((1, 42))
        self.data = np.array(df.values)
        self.player = self.extract_player(filename)
        self.turn = self.extract_turn(filename)
        self.move = self.extract_move(filename)
        self.score_1 = self.extract_score_1(filename)
        self.score_2 = self.extract_score_2(filename)

    def extract_move(self, filename):
        pattern = re.compile(r'sc_(\d)')
        match = pattern.search(filename)
        index = np.zeros((1,7), dtype=int)
        if match:
            move = int(match.group(1))
            index[0][move-1] = 1
        return index
        
    def extract_player(self, filename):
        pattern = re.compile(r't_(\d+)')
        match = pattern.search(filename)
        if match:
            turn = int(match.group(1))
            if turn%2 == 0:
                return 2
            else:
                return 1
            
    def extract_turn(self, filename):
        pattern = re.compile(r't_(\d+)')
        match = pattern.search(filename)
        if match:
            turn = int(match.group(1))

        return turn

    def extract_score_1(self, filename):
        score1 = 0
        pattern = re.compile(r'p1_(\d+)')
        match = pattern.search(filename)
        if match:
            score1 = int(match.group(1))
        pattern = re.compile(r'p2_(\d+)')

        return score1
        
    def extract_score_2(self, filename):
        score2 = 0
        pattern = re.compile(r'p2_(\d+)')
        match = pattern.search(filename)
        if match:
            score2 = int(match.group(1))

        return score2
    
### Testing
if __name__ == "__main__":
    mrg = TrainingDataHandler('data')

    # for i in mrg.list_of_datafiles:
    #     print(i)

    for i in mrg.list_of_datafiles:
        mrg.handler_get_state(i)
        print("Data:")
        print(mrg.data)
        print("Chosen collumn:")
        print(mrg.move)
        print("Player:")
        print(mrg.player)
        print("Turn:")
        print(mrg.turn)
        print("Player1 score:")
        print(mrg.score_1)
        print("Player2 score:")
        print(mrg.score_2)