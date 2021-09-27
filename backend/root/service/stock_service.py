from datetime import timedelta, datetime

from keras import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
from sklearn.preprocessing import MinMaxScaler

from ..config.lstm_model import conf
import numpy as np
import pandas as pd
import FinanceDataReader as fdr

from ..exception.handler import handler


class Service:
    model = None
    def __init__(self):
        def make_model(feature_shape, dropout=0.0):
            model = Sequential()
            model.add(LSTM(128,
                           input_shape=(feature_shape[1], feature_shape[2]),  # Time Steps, Variables
                           activation='relu',
                           return_sequences=True
                           )
                      )
            model.add(LSTM(128, activation='relu', return_sequences=True))
            model.add(LSTM(16, activation='relu', return_sequences=False))

            model.add(Dropout(dropout))
            model.add(Dense(len(self.config.scale_cols)))
            model.add(Activation('softmax'))

            return model

        self.config = conf()

        Service.model = make_model([1, self.config.WINDOW_SIZE, len(self.config.scale_cols)], dropout=0.0)
        Service.model.load_weights(self.config.WEIGHT_FILE)

    def get_today(self, symbol):
        df = fdr.DataReader(symbol, datetime.today().date() + timedelta(days=-10))
        print(df)
        fdr_data = dict()
        for e in df.keys():
            if e == 'Change': continue
            fdr_data[e] = int(df[e].values[-1])

        return fdr_data

    def predict(self, symbol):
        WINSIZE = self.config.WINDOW_SIZE
        def make_test_dataset(data, window_size):
            feature_list = []
            for i in range(len(data) - window_size + 1):
                feature_list.append(np.array(data.iloc[i:i + window_size]))  # WINDOW_SIZE 만큼의 데이터씩 담기
            return np.array(feature_list)

        # 종목 과거 데이터 추출
        prev_day = datetime.today() - timedelta(days=200)
        df = fdr.DataReader(symbol, prev_day)

        # Data Length Check
        if len(df) <= WINSIZE + self.config.FORECAST:
            handler.code(404, "this stock's deal duration is too short")

        # Data PreProcessing
        real = df[-WINSIZE - self.config.FORECAST:len(df)]
        test = self.pre_processing(real)[WINSIZE:]

        scaler_test = MinMaxScaler()

        scaler_test.fit(test[self.config.scale_cols])
        df_scaled = scaler_test.transform(test[self.config.scale_cols])
        df_scaled = pd.DataFrame(df_scaled, columns=self.config.scale_cols, index=list(test.index.values))

        test_feature = make_test_dataset(df_scaled, WINSIZE)

        # 모델로 FORECAST 만큼 예측하기
        for i in range(self.config.FORECAST):
            print(test_feature.shape)
            test_input = test_feature[0][i:].reshape(1, WINSIZE, len(self.config.scale_cols))
            pred = Service.model.predict(test_input)

            while abs(pred[0][0]) < abs(pred[0][2]):
                pred[0][0] += 0.000000001
                pred[0][0] *= 2
            while abs(pred[0][2]) * 10 < 0.4:
                pred[0][2] += 0.000000001
                pred[0][2] *= 10

            test_feature = np.insert(test_feature, WINSIZE + i, pred[0], axis=1)
            de_scaled_feature = scaler_test.inverse_transform(test_feature[0])

            if de_scaled_feature[WINSIZE + i][1] >= 0.5:
                pred[0][0] += pred[0][2]
            else:
                pred[0][0] -= pred[0][2]

            test_feature[0][WINSIZE + i][0] = pred[0][0]

            test_feature = test_feature.reshape(1, WINSIZE + (i + 1), len(self.config.scale_cols))

        test_feature[0] = scaler_test.inverse_transform(test_feature[0])

        predict_stock = test['Close']
        for i in range(self.config.FORECAST):
                predict_stock = np.append(predict_stock, test_feature[0][WINSIZE + i][0])

        return predict_stock




    def pre_processing(self, real):
        real['Updown'] = real['Close'] - real['Open']
        for i in range(len(real['Updown'])):
            real['Updown'].iloc[i] = 1 if real['Updown'][i] >= 0 else 0

        diff = abs(real['Close'][1:].values - real['Close'][0:-1].values)
        diff = np.insert(diff, 0, 0, axis=0)
        real['Diff'] = diff

        befo = real['Close'][1:].values - real['Close'][0:-1].values
        for i in range(0, len(real['Close']) - 1):
            if real['Close'][i + 1] - real['Close'][i] >= 0:
                befo[i] = 1
            else:
                befo[i] = 0
        befo = np.insert(befo, 0, 0, axis=0)
        real['Befo'] = befo

        return real


stock_service = Service()