"""for time series forcasting."""
import numpy as np


class forecasting():
    def bollinger_bands(period,data):

        data['sma'] = data['predicted'].rolling(period).mean()
        data['std'] = data['predicted'].rolling(period).std()
        data['upper'] = data['sma']+(data['std']*2)
        data['lower'] = data['sma']-(data['std']*2)

        return data

    def get_signal(data):
        buy_signal = []
        sell_signal = []
        for i in range(len(data['predicted'])):
            if data['predicted'][i]>data['upper'][i]:
                buy_signal.append(np.nan)
                sell_signal.append(data['predicted'][i])
            elif data['predicted'][i]<data['lower'][i]:
                buy_signal.append(data['predicted'][i])
                sell_signal.append(np.nan)
            else:
                buy_signal.append(np.nan)
                sell_signal.append(np.nan)

        return (buy_signal, sell_signal)