import asyncio

import requests
import zipfile
from io import BytesIO

import typing
import xmltodict
import json
from bs4 import BeautifulSoup
import OpenDartReader
import socket
import threading
import time

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session

from ..database import stock_crud
from ..exception.handler import handler
from ..model import opendart
from ..schema import stock
from ..database.conn import db
from ..service.stock_service import stock_service
from ..service.dart_service import dart_service
from ..service.kiwoom_service import k_win

# from ..schema.hoga import hoga

router = APIRouter()

host = "3.37.16.32"
port = 4500

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
    last_and_predict_stock, predict_stock = stock_service.predict(symbol)
    print("predict_stock: ", len(predict_stock))
    print(predict_stock)

    day = []
    ret = dict()

    for i, e in enumerate(predict_stock):
        day.append('D+' + str(i + 1))

    ret['close'] = predict_stock
    ret['date'] = day
    return ret


@router.get("/last")
async def get_last_price(symbol: str, duration: int):
    date, close = stock_service.get_last_price(symbol, duration)

    ret = dict()
    ret['date'] = date
    ret['close'] = close
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



# DB에서 요청 symbol 종목 호가 데이터 반환받기
@router.get("/realtime_hoga")
async def get_realtime_hoga(symbol: str, db: Session = Depends(db.get_db)):
    ret = stock_crud.get_hoga(db, symbol)

    return ret


# Client가 요청한 종목 실시간 호가 소켓 생성, 종목 등록
@router.post("/register_hoga")
async def register_hoga(symbol: str):
    msg = dict()
    msg['symbol'] = str(symbol)
    msg['method'] = "register"
    byte_msg = json.dumps(msg, indent=2).encode('utf-8')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))  # , port
    print("Server socket connected", host, port)
    server_socket.sendall(byte_msg)

    return "success"

# 실시간 호가 제거
@router.delete("/remove_hoga")
async def remove_hoga(symbol: str):
    msg = dict()
    msg['symbol'] = str(symbol)
    msg['method'] = "remove"
    byte_msg = json.dumps(msg, indent=2).encode('utf-8')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))  # , port
    print("Server socket connected", host, port)
    server_socket.sendall(byte_msg)

    return "success"


# 서비스에 사용하지 않음
@router.get("/insert_opendart_financial_info")
def insert_financial_info(db: Session = Depends(db.get_db)):
    corpInfo = None
    res = requests.get(url, params={'crtfc_key': api_key})
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
