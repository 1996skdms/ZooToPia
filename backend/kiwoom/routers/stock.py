import json
import socket

from fastapi import APIRouter, Depends, WebSocket, FastAPI
from sqlalchemy.orm import Session

from exception.handler import handler
from database.conn import db
from service.kiwoom import k_win

router = APIRouter()
app = FastAPI()

host = "127.0.0.1"
port = 4000

# Client와 Socket 연결하기
@router.websocket("/hoga/{symbol}")
async def get_hoga(symbol: str, client_socket: WebSocket, db: Session = Depends(db.get_db)):
    print("symbol : ", symbol)
    await client_socket.accept()

    if symbol is None:
        handler.code(404)

    # Kiwoom API와 소켓 통신 만들기
    msg = dict()
    msg['symbol'] = str(symbol)
    msg['method'] = "get_hoga"
    byte_msg = json.dumps(msg, indent=2).encode('utf-8')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.connect((host, port))
    server_socket.sendall(byte_msg)
    print("socket Init")
    cnt = 0
    while True:
        if cnt > 200:
            break
        cnt += 1
        print(cnt)
        ask, bid = k_win.getTenTimeHoga(server_socket)

        await client_socket.send_json(ask)
        await client_socket.send_json(bid)
        if len(ask) == 0:
            break

    print("서버 소켓 닫음")
    await client_socket.close()
    server_socket.close()



@router.get("/last/{symbol}")
def get_last(symbol: str, db: Session = Depends(db.get_db)):

    if symbol is None:
        handler.code(404)
    return k_win.getLastPrice(symbol=symbol)

