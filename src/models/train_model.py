"""Time series models."""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.initializers import he_uniform

class timeseriesmodels():
    def lstm_model(input,features):
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences = True, input_shape=(input, features)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(1, kernel_initializer = he_uniform()))
        model.compile(optimizer='adam', loss='mse')
        model.summary()

        return model