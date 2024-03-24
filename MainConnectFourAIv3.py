import numpy as np
from keras.models import Sequential, save_model, load_model
from keras.optimizers import Adam
from keras.layers import Dense, LeakyReLU, Dropout, Flatten, Reshape, Conv2D, MaxPooling2D
from keras.utils import to_categorical

from TrainingDataHandler import TrainingDataHandler
from AnalyzeLayout import AnalyzeLayout

class ConnectFourAI:
    def __init__(self,  pl_1_savefl, pl_2_savefl):
        self.model_1 = self.build_model()
        self.model_2 = self.build_model()

        self.model_1_saved_filename = pl_1_savefl
        self.model_2_saved_filename = pl_2_savefl

        self.analyzer = AnalyzeLayout()

    def build_model(self):
        model = Sequential()
        model.add(Reshape((6,7,1), input_shape=(42,)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(7, activation='softmax'))
        # model.add(Dense(7, activation='linear'))  # Single output neuron for the score

        optimizer = Adam(lr=0.001)
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        # optimizer = Adam(lr=0.0001)  # Adaptive stuff was 001
        # model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mae'])

        return model

    def reshape_board_to_input(self, board):
        input_array = np.array(board).reshape((1, 42))
        return input_array        

    def action_to_output(self, move):
        output_array = np.zeros((1, 7), dtype=int)
        output_array[0, move-1] = 1
        return output_array
    
    #
    def make_move(self, state):
        action_probabilities = self.model.predict(self.reshape_board_to_input(state))[0]
        valid_moves = self.get_valid_moves(state)
        legal_action_probabilities = action_probabilities * valid_moves
        return np.argmax(legal_action_probabilities) # Index chosen need to add 1 


    def get_valid_moves(self, board):
        valid_moves_array = np.ones((1,7), dtype=int)
        for i in range(0,6):
            if board[0][i] != 0:
                valid_moves_array[0][i] = 0
            else:
                continue
        return valid_moves_array
    # def train_player(self, model, X_train, y_train, epochs=100):
    #     model.fit(X_train, y_train, epochs=epochs, verbose=0)

    def train_player_1(self, model, X_train, y_train, num_samples, epochs=100):
        for epoch in range(epochs):
            for i in range(num_samples):
                state = self.get_next_gamestate()  # Replace with your function to get the next game state
                action = model.predict(self.reshape_board_to_input(state))
                reward = self.get_reward(state, action)  # Replace with your function to get the reward
                model.train_on_batch(self.reshape_board_to_input(state), self.action_to_output(action), sample_weight=reward) 

    def train_player_2(self, model, X_train, y_train, num_samples, epochs=100):
        for epoch in range(epochs):
            for i in range(num_samples):
                state = self.get_next_gamestate()  # Replace with your function to get the next game state
                action = model.predict(self.reshape_board_to_input(state))
                reward = self.get_reward(state, action)  # Replace with your function to get the reward
                model.train_on_batch(self.reshape_board_to_input(state), self.action_to_output(action), sample_weight=reward) 

    def simulate_action(self, current_state, collumn, player):
        simulated_move = current_state
        for i in range(5,-1,-1):
            if simulated_move[i][collumn] == 0:
                simulated_move[i][collumn] = player
                return simulated_move
            else:
                if i == 0:
                    #raise ValueError("Collumn is already filled to the top")
                    return False #Need to add some safer way to handle exeption here
                else:
                    continue

    def get_next_gamestate(self, current_state, chosen_action, player):
        next_state = self.simulate_action(current_state, chosen_action, player)
        return next_state

    def get_reward(self, current_state, chosen_action):
        next_state = self.simulate_action(current_state, chosen_action)
        if self.analyzer.run_win_check(next_state) == 1:
            return -1.0  # Player 1 is winning

        if self.analyzer.run_win_check(next_state) == 2:
            return 1.0  # Player 2 is winning

        if self.analyzer.run_win_check(next_state) == 3:
            return 0    #Draw
        
        self.analyzer.reset_analyzer()
        self.analyzer.analyzeBoard(next_state)
        if self.analyzer.playerTWOscore > self.analyzer.playerONEscore:
            return 0.1
        elif self.analyzer.playerONEscore > self.analyzer.playerTWOscore:
            return -0.1
        else:
            return 0

    def predict_player(self, model, board):
        input_board = self.reshape_board_to_input(board)
        prediction = model.predict(np.array([input_board]))
        return np.argmax(prediction)
    


    def save_model_as(self, name, model):
        save_model(model, "{0}{1}".format(name,".h5"))

    def load_model_v1(self):
        self.model_1 = load_model(self.model_1_saved_filename)
        self.model_2 = load_model(self.model_2_saved_filename)

    # def look_for_win_move_simulated(self, board):
    #     self.analyzer.run_win_check(board)



"""
So there is a problem with simulating game for ai to leatn, but hopefully in the matter of days i will manage to overcome those issues
Not really sure wether to use my existing evaluation tehnique or to write completly new one.
"""