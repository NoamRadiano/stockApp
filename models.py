from copy import deepcopy
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from keras.models import Sequential
from keras import layers
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split, TimeSeriesSplit
import yfinance as yf


def calcol_percentage(close, open):
    num = (close - open) / open
    return num


def calcol_neg_per(close, open):
    if (close - open < 0):
        return True
    else:
        return False


class makePredictionModel:
    # if someone wants specific day, he has to validate that the start date starts on the same day and ends at the same day
    def __init__(self, stock_symbol='MSFT', start_date='2022-05-02', end_date=' ', interval='1d', day=None):
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        stock = yf.Ticker(stock_symbol)
        self.data = stock.history(period='max', interval='1d')
        self.data = self.data.reset_index()
        # parse dates making the dates in column 0 from string to datetime object
        self.data['Date'] = self.data['Date'].to_numpy().astype('datetime64')
        # making new column for each day verses the date
        self.data["Day In Week"] = self.data['Date'].dt.day_name()
        self.change_data()
        self.dates, self.X, self.y = self.windowed_df_to_date_X_y()
        self.prediction = self.make_model()

    def change_data(self):
        self.data['Movement%'] = np.vectorize(calcol_percentage)(
            self.data['Close'], self.data['Open'])
        df_fordays = pd.DataFrame(self.data['Day In Week'])
        days_df = df_fordays.select_dtypes(include='object')
        rest_of_df = self.data.drop('Day In Week', axis=1)
        df_objects_dummies = pd.get_dummies(days_df)
        self.final_df = pd.concat([rest_of_df, df_objects_dummies], axis=1)
        self.data = self.final_df
        # knowing corr between movement to the other columns
        self.data = self.data.drop('Dividends', axis=1)
        self.data['Day In Week'] = self.data['Date'].dt.day_name()
        self.data['Date'] = self.data['Date'].astype('datetime64[ns]').dt.strftime(
            '%Y-%m-%d').astype('datetime64[ns]')
        self.data = self.data.set_index('Date')
        self.df = self.data[['Close']]
        ##
        # need to check if working
        # each day of week in week intervals or every day in day intervals
        # the diffrence is between self.day_df or self.df, if self.day_df so need self.day_in_week
        if (self.interval == '1d'):  # change it
            self.windowed_df = self.window_data(
                self.df, self.start_date, self.end_date, n=3)
        else:
            day_in_week_in_datetime = dt.datetime.strptime(
                self.start_date, '%Y-%m-%d')
            self.day_in_week = day_in_week_in_datetime.strftime('%A')
            self.day_df = self.data[self.data[f"Day In Week_{self.day_in_week}"] == True]
            self.day_df = self.day_df[['Close']]
            self.windowed_df = self.window_data(
                self.day_df, self.start_date, self.end_date, n=3)

    def window_data(self, data, start_date, end_date, n=3):
        windowed_data = pd.DataFrame()
        for i in range(n, 0, -1):
            windowed_data[f'Target-{i}'] = data['Close'].shift(i)
        windowed_data['Target'] = data['Close']
        windowed_data = windowed_data.loc[start_date:end_date]
        windowed_data = windowed_data.reset_index()
        windowed_data.rename(columns={'Date': 'Target Date'}, inplace=True)
        return windowed_data.dropna()

    def windowed_df_to_date_X_y(self):
        df_as_np = self.windowed_df.to_numpy()
        dates = df_as_np[:, 0]
        middle_matrix = df_as_np[:, 1:-1]
        X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))
        Y = df_as_np[:, -1]
        return dates, X.astype(np.float32), Y.astype(np.float32)

    def make_model(self):
        q_80 = int(len(self.dates) * .8)
        q_90 = int(len(self.dates) * .9)

        self.dates_train, self.X_train, self.y_train = self.dates[:
                                                                  q_80], self.X[:q_80], self.y[:q_80]

        self.dates_val, self.X_val, self.y_val = self.dates[q_80:
                                                            q_90], self.X[q_80:q_90], self.y[q_80:q_90]
        self.dates_test, self.X_test, self.y_test = self.dates[q_90:], self.X[q_90:], self.y[q_90:]

        model = Sequential([layers.Input((3, 1)),
                            layers.LSTM(64),
                            layers.Dense(32, activation='relu'),
                            layers.Dense(32, activation='relu'),
                            layers.Dense(1)])

        model.compile(loss='mse',
                      optimizer=Adam(learning_rate=0.001),
                      metrics=['mean_absolute_error'])

        model.fit(self.X_train, self.y_train, validation_data=(
            self.X_val, self.y_val), epochs=100)

        self.train_predictions = model.predict(self.X_train).flatten()
        self.val_predictions = model.predict(self.X_val).flatten()
        self.test_predictions = model.predict(self.X_test).flatten()

        # prediction of the next day\week
        predictions_values = []
        predict_days = []
        new_array_values = []
        tst = np.array(
            [[self.y_test[-3]], [self.y_test[-2]], [self.y_test[-1]]])
        # check y_test(tst) or X_text[-1] in deepcopy 1 line down below
        predictions_array_for_predict = [deepcopy(self.X_test[-1])]
        for i in range(1, 2):  # range is the number of predictions
            predict_days.append(self.dates_test[-1] + dt.timedelta(days=i))
            next_prediction = model.predict(
                np.array(predictions_array_for_predict))
            predictions_values.append(next_prediction)
            predictions_array_for_predict[0][-3] = predictions_array_for_predict[0][-2]
            predictions_array_for_predict[0][-2] = predictions_array_for_predict[0][-1]
            predictions_array_for_predict[0][-1] = [next_prediction]
        # range is the number of predictions, has to be 1 less then the range above
        for i in range(0, 1):
            new_array_values.append(predictions_values[i][0][0])
        return new_array_values[0]
