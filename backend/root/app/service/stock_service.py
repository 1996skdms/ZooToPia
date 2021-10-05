from datetime import timedelta, datetime
import os

from keras.models import load_model
from keras.layers import LSTM, Dropout, Dense, Activation
from sklearn.preprocessing import MinMaxScaler

from ..config.lstm_model import conf
import numpy as np
import pandas as pd
import FinanceDataReader as fdr

from ..exception.handler import handler
import tensorflow as tf
import pymysql

mysql_db = pymysql.connect(
    user="root",
    passwd="1234",
    host="j5a602.p.ssafy.io",
    port=3306,
    db="bigdata",
    charset="utf8"
)
my_devices = tf.config.experimental.list_physical_devices(device_type='GPU')
tf.config.experimental.set_visible_devices(devices= my_devices, device_type='GPU')

class Service:
    model3 = None
    model7 = None
    def __init__(self):
        def make_model():
            model3 = load_model(os.getcwd() + self.config.MODEL3)
            model7 = load_model(os.getcwd() + self.config.MODEL7)

            return model3, model7

        self.config = conf()

        Service.model3, Service.model7 = make_model()
        print(os.getcwd() + self.config.WEIGHT_FILE3)
        Service.model3.load_weights(os.getcwd() + self.config.WEIGHT_FILE3)
        Service.model7.load_weights(os.getcwd() + self.config.WEIGHT_FILE7)

    def get_today(self, symbol):
        df = fdr.DataReader(symbol, datetime.today().date() + timedelta(days=-10))
        print(df)
        fdr_data = dict()
        for e in df.keys():
            if e == 'Change': continue
            fdr_data[e] = int(df[e].values[-1])

        return fdr_data

    def get_last_price(self, symbol, duration):
        df = fdr.DataReader(symbol, datetime.today().date() + timedelta(days=-duration))

        date = []
        close = []

        for i in range(len(df)):
            date.append(str(datetime.date(df.index[i])))
            close.append(int(df['Close'][i]))

        return date, close

    def predict(self, symbol):
        def make_test_dataset(data, window_size):
            feature_list = []
            for k in range(len(data) - window_size + 1):
                feature_list.append(np.array(data.iloc[k:k + window_size]))  # WINDOW_SIZE 만큼의 데이터씩 담기
            return np.array(feature_list)

        cursor = mysql_db.cursor(pymysql.cursors.DictCursor)
        sql = "select * from stock where symbol like '" + symbol + "%'"
        cursor.execute(sql)
        stock_meta_data = cursor.fetchall()[0]

        model = None
        scale_cols = None
        if stock_meta_data['NAME'] in ['005930', '035720', '068270']:           # 뉴스 데이터 분석 포함 예측 모델 사용
            model = self.model3
            scale_cols = self.config.scale_cols4
        else:
            model = self.model7
            scale_cols = self.config.scale_cols3

        predict_from_prev_day = 0

        prev_day = datetime.today() - timedelta(days=200)
        df = fdr.DataReader(stock_meta_data['symbol'], prev_day)

        if len(df) <= self.config.WINDOW_SIZE + self.config.FORECAST: return []

        real = df[-self.config.WINDOW_SIZE - predict_from_prev_day: - predict_from_prev_day]
        if predict_from_prev_day == 0: real = df[-self.config.WINDOW_SIZE - predict_from_prev_day:]
        real_compare = df[-self.config.WINDOW_SIZE - predict_from_prev_day:]

        print("0")
        search_start_date = datetime.today().date() - timedelta(days=self.config.WINDOW_SIZE * 5)
        sql = "select date_format(date, '%Y-%m-%d') AS date, score" \
              " FROM stock_posi_negative" \
              " WHERE stock_posi_negative.code LIKE '" + str(
              stock_meta_data['symbol']) + "' AND date >= DATE('" + str(search_start_date) + "') " \
              " ORDER BY date"
        print("1")
        cursor.execute(sql)
        score_df = cursor.fetchall()[-self.config.WINDOW_SIZE - predict_from_prev_day:]
        print(score_df)

        print("2")
        tmp_df = []
        for e in real.index:
            flag = False
            for e2 in score_df:
                if str(e2['date']) == str(datetime.date(e)):
                    flag = True
                    tmp_df.append(e2['score'])
                    break
            if flag is False:
                tmp_df.append(0.52)

        real['Score'] = tmp_df

        scaler_real = MinMaxScaler()  # 정규화 : 데이터를 0 ~ 1 로 정규화

        scaler_real.fit(real[scale_cols])
        real_scaled = scaler_real.transform(real[scale_cols])
        real_scaled = pd.DataFrame(real_scaled, columns=scale_cols, index=list(real.index.values))
        test_feature = make_test_dataset(real_scaled, self.config.WINDOW_SIZE)

        for i in range(self.config.FORECAST):
            test_input = test_feature[0][i:].reshape(1, self.config.WINDOW_SIZE, len(scale_cols))
            print(i)
            pred = model.predict(test_input)

            test_feature = np.insert(test_feature, self.config.WINDOW_SIZE + i, pred[0], axis=1)
            de_scaled_feature = scaler_real.inverse_transform(test_feature[0])
            # print(de_scaled_feature[self.config.WINDOW_SIZE + i])

            test_feature = test_feature.reshape(1, self.config.WINDOW_SIZE + (i + 1), len(scale_cols))

        de_scaled = scaler_real.inverse_transform(test_feature[0])

        return de_scaled[:, 1], list(map(int, de_scaled[-self.config.FORECAST:, 1]))


stock_service = Service()