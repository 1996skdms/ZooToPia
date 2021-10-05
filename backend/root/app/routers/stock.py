import requests
import zipfile
from io import BytesIO
import xmltodict
import json
from bs4 import BeautifulSoup
import OpenDartReader
import socket

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
async def stock_predict(name: str):
    if name is None: handler.code(404)
    last_and_predict_stock, predict_stock = stock_service.predict(name)
    print("predict_stock: ", len(predict_stock))
    print(predict_stock)

    day = []
    ret = dict()

    for i, e in enumerate(predict_stock):
        day.append('D+' + str(i+1))

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
    print("종목 금일 데이터: ", today)

    return today


@router.get("/financial_info")
async def get_financial_info(name: str, db: Session = Depends(db.get_db)):
    dart = OpenDartReader(api_key=api_key)

    stock_profile = await get_stock_profile(name, db)

    return dart_service.financial_info(dart, stock_profile.symbol)


# Client와 Socket 연결하기
@router.websocket("/hoga/{symbol}")
async def get_hoga(symbol: str, client_socket: WebSocket, db: Session = Depends(db.get_db)):
    print("symbol : ", symbol)
    await client_socket.accept()
    print("Front Client Socket accepted")
    if symbol is None:
        handler.code(404)

    # Kiwoom API와 소켓 통신 만들기
    msg = dict()
    msg['symbol'] = str(symbol)
    msg['method'] = "get_hoga"
    byte_msg = json.dumps(msg, indent=2).encode('utf-8')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server socket connection waiting:", host, port)
    server_socket.connect((host, port))               #, port
    print("Server socket connected")
    server_socket.sendall(byte_msg)
    print("socket Init")
    cnt = 0
    while True:
        if cnt > 10:
            break
        cnt += 1
        print("Server: 프로그램에 소켓 통신 요청", cnt, "번째")
        ask, bid = k_win.getTenTimeHoga(server_socket)

        if len(ask) == 0:
            print("Server: 호가 정보 없음.")
            break

        print("Server: 프론트로 호가 정보 전송 전")
        try:
            await client_socket.send_json(ask)
            await client_socket.send_json(bid)
            print("Server: 프론트로 호가 정보 전송 완료")
        except:
            break


    print("서버 소켓 닫음")
    await client_socket.close()
    server_socket.close()


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

