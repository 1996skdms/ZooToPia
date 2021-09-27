from datetime import datetime, timedelta
import requests
import zipfile
from io import BytesIO
import xmltodict
import json
from bs4 import BeautifulSoup
import OpenDartReader

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config.lstm_model import Config
from ..database import stock_crud
from ..exception.handler import handler
from ..model import opendart
from ..schema import stock
from ..database.conn import db
from ..schema.predict import Predict
from ..service.stock_service import stock_service
from ..service.dart_service import dart_service

router = APIRouter()

url = 'https://opendart.fss.or.kr/api/corpCode.xml'
api_key = '5f7647c213c1aa874a889ff66a791412bc1020b7'

@router.get("/symbol", response_model=stock.Stock)
async def get_stock_profile(name: str, db: Session = Depends(db.get_db)):
    if name is None:
        handler.code(404)

    stock_profile = stock_crud.get_symbol(db, name=name)

    return stock_profile


@router.get("/predict")
async def stock_predict(symbol: str):
    if symbol is None: handler.code(404)
    predict_stock = stock_service.predict(symbol)

    conf = Config()
    pred = Predict()
    ret = dict()

    for i, e in enumerate(predict_stock):
        pred.price.append(int(e))
        pred.day.append(datetime.today().date() + timedelta(conf.FORECAST - len(predict_stock) + i + 1))

    ret['price'] = pred.price
    ret['day'] = pred.day
    return ret


@router.get("/today")
async def get_today(symbol: str):
    if symbol is None or len(symbol) == 0:
        handler.code(404)

    today = stock_service.get_today(symbol)
    print(today)

    return today


@router.get("/financial_info")
async def get_financial_info(name: str, db: Session = Depends(db.get_db)):
    dart = OpenDartReader(api_key=api_key)

    stock_profile = await get_stock_profile(name, db)

    return dart_service.financial_info(dart, stock_profile.symbol)






# 서비스에 사용하지 않음
@router.get("/insert_opendart_financial_info")
def insert_financial_info(db: Session = Depends(db.get_db)):
    corpInfo = None
    res = requests.get(url, params={'crtfc_key': key})
    with zipfile.ZipFile(BytesIO(res.content)) as zf:
        file_list = zf.namelist()
        while len(file_list) > 0:
            print("getCorp")
            file_name = file_list.pop()
            corpInfo = zf.open(file_name).read().decode()
            break

    soup = BeautifulSoup(corpInfo, 'html.parser')
    data_odict = xmltodict.parse(soup.prettify())
    data_dict = json.loads(json.dumps(data_odict))
    data = data_dict.get('result', {}).get('list')

    print(len(data))
    input("start ")
    cnt = 0
    for e in data:
        cnt += 1
        if cnt % 500 == 0: print(cnt)
        if e['stock_code'] is None: continue

        entity = opendart.Opendart(corp_code=e['corp_code'],
                                   corp_name=e['corp_name'],
                                   stock_code=e['stock_code'],
                                   modify_date=e['modify_date'])
        db.add(entity)
        db.commit()

    print("the end")

