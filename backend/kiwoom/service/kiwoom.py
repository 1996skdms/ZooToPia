import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *

import socket
import json
import ast

host = "127.0.0.1"
port = 4000

class MyWindow():
    def __init__(self):
        super().__init__()

    def getTenTimeHoga(self, client_socket):
        ask = client_socket.recv(1024)
        print(ask)
        print(len(ask))
        if len(ask) <= 2:
            return [], []
        ask = ast.literal_eval(ask.decode('utf-8'))
        ask_decode = ask[0]
        # ask_decode = ast.literal_eval(ask.decode('utf-8'))[0]
        bid = client_socket.recv(1024)
        bid_decode = ast.literal_eval(bid.decode('utf-8'))[0]

        return ask_decode, bid_decode

    def getLastPrice(self, symbol):
        pass


k_win = MyWindow()
