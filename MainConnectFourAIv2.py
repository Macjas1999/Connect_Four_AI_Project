import numpy as np
try:
    from tensorflow.keras.models import Sequential, save_model, load_model  # pyright: ignore[reportMissingImports]
    from tensorflow.keras.optimizers import Adam  # pyright: ignore[reportMissingImports]
    from tensorflow.keras.layers import Dense, LeakyReLU, Dropout, Flatten, Reshape, Conv2D, MaxPooling2D  # pyright: ignore[reportMissingImports]
    from tensorflow.keras.utils import to_categorical  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    from keras.models import Sequential, save_model, load_model  # pyright: ignore[reportMissingImports]
    from keras.optimizers import Adam  # pyright: ignore[reportMissingImports]
    from keras.layers import Dense, LeakyReLU, Dropout, Flatten, Reshape, Conv2D, MaxPooling2D  # pyright: ignore[reportMissingImports]
    from keras.utils import to_categorical  # pyright: ignore[reportMissingImports]

from TrainingDataHandler import TrainingDataHandler

class ConnectFourAI:
    def __init__(self,  pl_1_savefl, pl_2_savefl):
        self.model_1 = self.build_model()
        self.model_2 = self.build_model()

        self.model_1_saved_filename = pl_1_savefl
        self.model_2_saved_filename = pl_2_savefl


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

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        # optimizer = Adam(lr=0.0001)  # Adaptive stuff was 001
        # model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mae'])

        return model

    def board_to_input(self, board):
        return np.array(board).reshape(1, 42) #not using flatten() becouse it creates 1D array
    


    def train_player(self, model, X_train, y_train, epochs=100):
        model.fit(X_train, y_train, epochs=epochs, verbose=0)

    def predict_player(self, model, board):
        input_board = self.board_to_input(board)
        prediction = model.predict(np.array([input_board]))
        return np.argmax(prediction)
    


    def save_model_as(self, name, model):
        save_model(model, "{0}{1}".format(name,".h5"))

    def load_model_v1(self):
        self.model_1 = load_model(self.model_1_saved_filename)
        self.model_2 = load_model(self.model_2_saved_filename)
