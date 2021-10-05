from pydantic.dataclasses import dataclass
import os

@dataclass
class Config:
    scale_cols4 = ['Open', 'Close', 'Volume' , 'Score']                                # 변수   /  'Open', 'High', 'Low',
    cols4 = ['open', 'close', 'volume' , 'score']                                       # 'open', 'high', 'low',

    scale_cols3 = ['Open', 'Close', 'Volume']                                # 변수   /  'Open', 'High', 'Low',
    cols3 = ['open', 'close', 'volume']                                       # 'open', 'high', 'low',

    WINDOW_SIZE = 16                                                                      # 다음날 예측에 사용할 현재일로부터 ~ 과거 데이터 개수
    FORECAST = 15   # 앞으로 예측할 날 수

    MODEL3 = os.path.join('/app/model_file' + '/stock_model_3_news')
    MODEL7 = os.path.join('/app/model_file' + '/stock_model_7')

    WEIGHT_FILE3 = '/app/model_file' + '/Batch2_window16_dense4_lr0.002_128_64_16_ep63_News_3.h5'
    WEIGHT_FILE7 = '/app/model_file' + '/Batch2_window16_dense3_lr0.002_128_64_16_ep52_7.h5'


def conf():
    return Config

