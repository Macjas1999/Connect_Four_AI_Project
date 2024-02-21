import os
import pandas as pd
import numpy as np
import csv
import re

class TrainingDataHandler:
    def __init__(self, dir):
        self.directory = dir
        self.data = []
        self.labels_1 = []
        self.labels_2 = []

    def ext_player(self, filename):
        pattern = re.compile(r'p(\d)')
        match = pattern.search(filename)
        if match:
            return int(match.group(1))
        
    def extract_score_1(self, filename):
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
        return score1 - score2
        
    def extract_score_2(self, filename):
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

                df = pd.read_csv(os.path.join(self.directory, filename),index_col=None, header=None)
                flattened_array = df.values.flatten()
                self.data.append(flattened_array)

                self.labels_1.append(self.extract_score_1(filename))
                self.labels_2.append(self.extract_score_2(filename))

        self.data = np.array(self.data)
        self.labels_1 = np.array(self.labels_1)
        self.labels_2 = np.array(self.labels_2)

    def save_extracted(self, result_filename, player):
        #self.data = np.array(self.data)
        #self.labels = np.array(self.labels)
        if player == 1:
            merged_data = pd.DataFrame(np.concatenate((self.data, self.labels_1.reshape(-1, 1)), axis=1))
            merged_data.to_csv(result_filename, index=False, header=False)
        elif player == 2:
            merged_data = pd.DataFrame(np.concatenate((self.data, self.labels_2.reshape(-1, 1)), axis=1))
            merged_data.to_csv(result_filename, index=False, header=False)
        else:
            return
    def load_merged_data(self, target_filename):
        merged_data = pd.read_csv(target_filename, index_col=None, header=None)
        self.data = merged_data.iloc[:, :-1].values
        
    def load_merged_labels(self, target_filename, player):
        if player == 1:
            merged_data = pd.read_csv(target_filename, index_col=None, header=None)
            self.labels_1= merged_data.iloc[:, -1].values
        elif player == 2:
            merged_data = pd.read_csv(target_filename, index_col=None, header=None)
            self.labels_2= merged_data.iloc[:, -1].values


if __name__ == "__main__":
    mrg = TrainingDataHandler('data1')
    mrg.extract_data()
    mrg.save_extracted('resultextract_player1.csv', 1)
    mrg.save_extracted('resultextract_player1.csv', 2)
    #mrg.load_merged('resultextract.csv')
    print(mrg.data.shape)  # (num_samples, flattened_board_size)
    print(mrg.labels_1.shape)  # (num_samples, 2)
    print(mrg.labels_2.shape)
    #print(mrg.labels)
    news_1 = mrg.labels_1.reshape(-1, 1)
    news_2 = mrg.labels_2.reshape(-1, 1)
    print(news_1.shape)
    print(news_2.shape)
    test = [1, 2, 3, 4]
    test = np.array(test)
    print(test.shape)
    #print(mrg.data)