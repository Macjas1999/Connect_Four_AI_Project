import os
import pandas as pd
import numpy as np
import csv
import re

class TrainingDataHandler:
    def __init__(self, dir):
        self.directory = dir
        self.data = []
        self.labels = []

    def ext_player(self, filename):
        pattern = re.compile(r'p(\d)')
        match = pattern.search(filename)
        if match:
            return int(match.group(1))
        
    def extract_score(self, filename):
        score1 = 0
        score2 = 0
        pattern = re.compile(r'p1_(\d+)')
        match = pattern.search(filename)
        if match:
            score1 = int(match.group(1))
        pattern = re.compile(r'p2_(\d+)')
        match = pattern.search(filename)
        if match:
            score2 = int(match.group(1))
        return score2 - score1

    
    def extract_data(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".csv"):
                #player_number = self.ext_player(filename)

                df = pd.read_csv(os.path.join(self.directory, filename),index_col=None, header=None)
                flattened_array = df.values.flatten()
                self.data.append(flattened_array)

                self.labels.append(self.extract_score(filename))
                # if player_number == 1:
                #     self.labels.append(-1)
                #     #self.labels.append(1)
                # elif player_number == 2:
                #     self.labels.append(1)
                #     #self.labels.append(2)

        self.data = np.array(self.data)
        self.labels = np.array(self.labels)

    def save_extracted(self, result_filename):
        #self.data = np.array(self.data)
        #self.labels = np.array(self.labels)

        merged_data = pd.DataFrame(np.concatenate((self.data, self.labels.reshape(-1, 1)), axis=1))
        merged_data.to_csv(result_filename, index=False, header=False)

    def load_merged(self, target_filename):
        merged_data = pd.read_csv(target_filename, index_col=None, header=None)
        self.data = merged_data.iloc[:, :-1].values
        self.labels = merged_data.iloc[:, -1].values
        #
        #self.labels = self.labels.reshape(-1, 1)


if __name__ == "__main__":
    mrg = TrainingDataHandler('data1')
    mrg.extract_data()
    mrg.save_extracted('resultextract.csv')
    #mrg.load_merged('resultextract.csv')
    print(mrg.data.shape)  # (num_samples, flattened_board_size)
    print(mrg.labels.shape)  # (num_samples, 2)
    #print(mrg.labels)
    news = mrg.labels.reshape(-1, 1)
    print(news.shape)
    test = [1, 2, 3, 4]
    test = np.array(test)
    print(test.shape)
    #print(mrg.data)