import json
import ast
import socket

host = "3.37.16.32"
port = 4500


class Kiwoom():
    def __init__(self):
        super().__init__()

    def register_hoga(self, symbol):
        msg = dict()
        msg['symbol'] = str(symbol)
        msg['method'] = "register"
        byte_msg = json.dumps(msg, indent=2).encode('utf-8')

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))  # , port
        print("Server socket connected register", host, port)
        server_socket.sendall(byte_msg)

    def remove_hoga(self, symbol):
        msg = dict()
        msg['symbol'] = str(symbol)
        msg['method'] = "remove"
        byte_msg = json.dumps(msg, indent=2).encode('utf-8')

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))  # , port
        print("Server socket connected remove", host, port)
        server_socket.sendall(byte_msg)


k_win = Kiwoom()

