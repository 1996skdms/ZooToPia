import json
import ast

host = "127.0.0.1"
port = 4000

class Kiwoom():
    def __init__(self):
        super().__init__()

    def getTenTimeHoga(self, client_socket):
        print("Server : 호가 정보 받기 전 대기")
        ask = client_socket.recv(1024)
        if len(ask) <= 2:
            return [], []
        ask = ast.literal_eval(ask.decode('utf-8'))
        ask_decode = ask[0]
        # ask_decode = ast.literal_eval(ask.decode('utf-8'))[0]
        bid = client_socket.recv(1024)
        bid_decode = ast.literal_eval(bid.decode('utf-8'))[0]

        print("Server : 호가 정보 받음", ask_decode, bid_decode)
        return ask_decode, bid_decode

    def getLastPrice(self, symbol):
        pass


k_win = Kiwoom()

