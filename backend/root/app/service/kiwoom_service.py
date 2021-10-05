import asyncio
import json
import ast
import socket

# from ..schema.hoga import hoga

host = "3.37.16.32"
port = 4500


class Kiwoom():
    def __init__(self):
        super().__init__()

    def kiwoom_socket_th(self, symbol, loop):

        async def socket_excute():
            # await client_socket.accept()

            # Kiwoom API와 소켓 통신 만들기
            msg = dict()
            msg['symbol'] = str(symbol)
            msg['method'] = "get_hoga"
            byte_msg = json.dumps(msg, indent=2).encode('utf-8')

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Server socket connection waiting:", host, port)
            server_socket.connect((host, port))  # , port
            print("Server socket connected")
            server_socket.sendall(byte_msg)
            print("socket Init")

            cnt = 0
            while True:
                cnt += 1
                print("Server: 프로그램에 소켓 통신 요청", cnt, "번째")
                ask, bid = self.getTenTimeHoga(server_socket)

                # hoga[symbol].ask_price = ask['price']
                # hoga[symbol].ask_volume = ask['volume']
                # hoga[symbol].bid_price = bid['price']
                # hoga[symbol].bid_volume = bid['volume']
                # print(hoga[symbol])

                # if len(ask) == 0:
                #     print("Server: 호가 정보 없음.")
                #     break
                #
                # print("Server: 프론트로 호가 정보 전송 전")
                # try:
                #     print(client_socket.active_connections)
                #     await client_socket.send_json(ask)
                #     await client_socket.send_json(bid)
                #     # print("Server: 프론트로 호가 정보 전송 완료")
                # except Exception as e:
                #     print(e)
                #     break

            print("서버 소켓 닫음")
            # await client_socket.close()
            server_socket.close()

        loop.run_until_complete(socket_excute())

    def getTenTimeHoga(self, server_socket):
        print("Server : 호가 정보 받기 전 대기")
        try:
            server_socket.settimeout(5)                   # timeout 설정
            ask = server_socket.recv(1024)
            if len(ask) <= 2:
                return [], []
            ask = ast.literal_eval(str(ask.decode('utf-8')))
            ask_decode = ask[0]
            bid = server_socket.recv(1024)
            bid_decode = ast.literal_eval(str(bid.decode('utf-8')))[0]

            print("Server : 호가 정보 받음", ask_decode, bid_decode)
            print("Server : 호가 정보 받음", ask_decode, bid_decode)
            return ask_decode, bid_decode
        except socket.timeout:
            return [], []

    def getLastPrice(self, symbol):
        pass


k_win = Kiwoom()

