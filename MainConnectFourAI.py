import numpy as np
from keras.models import Sequential
from keras.models import save_model
from keras.models import load_model
from keras.layers import Dense
from keras.utils import to_categorical
from TrainingDataHandler import TrainingDataHandler

class ConnectFourAI:
    def __init__(self,  pl_1_savefl, pl_2_savefl):
        self.model_1 = self.build_model()
        self.model_2 = self.build_model()

        self.model_1_saved_filename = pl_1_savefl
        self.model_2_saved_filename = pl_2_savefl


    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=42, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(7, activation='linear'))  # Single output neuron for the score
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        return model

    def board_to_input(self, board):
        return np.array(board).flatten()

    def train_player(self, model, X_train, y_train, epochs=100):
        model.fit(X_train, y_train, epochs=epochs, verbose=0)

    def predict_player(self, model, board):
        input_board = self.board_to_input(board)
        prediction = model.predict(np.array([input_board]))
        return np.argmax(prediction)
    
    def save_model_as(self, name, model):
        save_model(model, "{0}{1}".format(name,".h5"))

    def train_only_save(self):
        datahand = TrainingDataHandler('data1')
        #datahand.extract_data()
        datahand.load_merged_data('resultextract_player1.csv')
        datahand.load_merged_labels('resultextract_player1.csv', 1)
        datahand.load_merged_labels('resultextract_player2.csv', 2)

        self.train_player(self.model_1, datahand.data, datahand.labels_1)
        self.train_player(self.model_2, datahand.data, datahand.labels_2)

        self.save_model_as("model_1_v1", self.model_1)
        self.save_model_as("model_2_v1", self.model_2)

    def load_model_v1(self):
        self.model_1 = load_model(self.model_1_saved_filename)
        self.model_2 = load_model(self.model_2_saved_filename)