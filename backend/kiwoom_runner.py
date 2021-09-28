import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from pykiwoom.kiwoom import *
from PyQt5.QtCore import *

import json
import ast
import socket
import threading
import time
host = "127.0.0.1"
port = 4000

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.k = Kiwoom()

        self.ask = dict()
        self.bid = dict()
        self.time = dict()

        self.setWindowTitle("주식호가잔량")
        self.setGeometry(300, 300, 300, 400)

        btn = QPushButton("구독", self)
        btn.move(20, 20)
        btn.clicked.connect(self.btn_clicked)

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.dynamicCall("CommConnect()")

        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        self.ocx.OnReceiveTrData.connect(self._handler_tr_data)
        self.ocx.OnReceiveMsg.connect(self._handler_msg_data)
        self.ocx.OnReceiveChejanData.connect(self._handler_chejan_data)
        self.ocx.OnReceiveTrCondition.connect(self._handler_trc_data)

        self.th = Worker(1, self)
        self.th.threadEvent.connect(self.threadEventHandler)
        self.th.start()

    @pyqtSlot(int)
    def threadEventHandler(self, n):
        print('메인 : threadEvent(self,' + str(n) + ')')

    # 특정 Client와 연결된 상태
    def handle_client(self, client_socket, addr):
        print("Client's Addr :", addr)
        req = client_socket.recv(256)
        req_decode = ast.literal_eval(req.decode('utf-8'))
        if req_decode['method'] == 'get_hoga':
            self.getTenTimeHoga(req_decode['symbol'])

            while True:
                time.sleep(1)         # 1초마다 발신
                try:
                    if len(self.ask[req_decode['symbol']]) == 0:
                        client_socket.send(json.dumps([]).encode('utf-8'))
                        raise Exception
                    byte_msg = json.dumps(self.ask[req_decode['symbol']], indent=2).encode('utf-8')
                    client_socket.send(byte_msg)
                    byte_msg = json.dumps(self.bid[req_decode['symbol']], indent=2).encode('utf-8')
                    client_socket.send(byte_msg)
                except Exception as e:
                    print("Program: 소켓 닫음.")
                    self.removeTenTimeHoga(req_decode['symbol'])
                    client_socket.close()
                    break

    def init_socket(self):
        print("init_socket")
        global server_socket

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((host, port))
        server_socket.listen(1000)
        while True:
            print("Program: 소켓 연결 대기")
            client_socket, addr = server_socket.accept()
            print("Program: 소켓 연결 요청 허가")
            t = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            t.daemon = True                 # 데몬 프로세스로 실행 ( 부모가 종료되면 함께 종료 )
            t.start()

    def btn_clicked(self):
        self.getTenTimeHoga("005930")
        # df = self.k.block_request("opt10001",
        #                           종목코드="005930",
        #                           output="주식기본정보",
        #                           next=0)
        # print(df)

    def _handler_login(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("login 완료")

    def _handler_real_data(self, code, real_type, data):
        print(code, real_type)

        if real_type == "ECN주식호가잔량":
            self.ask[str(code)] = []
            self.bid[str(code)] = []
        if real_type == "주식호가잔량":
            ask, bid = dict(), dict()
            ask['price'], ask['volume'] = [], []
            bid['price'], bid['volume'] = [], []
            for i in range(1, 11):
                ask['price'].append(self.GetCommRealData(code, 40 + i))
                ask['volume'].append(self.GetCommRealData(code, 60 + i))
                ask['updown'] = 'ask';
                bid['price'].append(self.GetCommRealData(code, 50 + i))
                bid['volume'].append(self.GetCommRealData(code, 70 + i))
                bid['updown'] = 'bid';

            self.ask[str(code)], self.bid[str(code)] = [], []
            self.ask[str(code)].append(ask)
            self.bid[str(code)].append(bid)

            print(self.ask[str(code)])
            print(self.bid[str(code)])

    def getLastPrice(self, code):
        self.ocx.dynamicCall("GetMasterLastPrice(QString)", [int(code)])

    def getTenTimeHoga(self, symbol):
        print("get hoga register")
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                             "1000", str(symbol), "41", 1)  # screen_no, code_list, fid_list, real_type

    def removeTenTimeHoga(self, symbol):
        self.ocx.dynamicCall("SetRealRemove(QString, QString, QString, QString)",
                             "1000", str(symbol))

    def _handler_tr_data(self, code, real_type, data):
        print("_handler_tr_data", code)

    def _handler_msg_data(self, code, real_type, data):
        print("OnReceiveMsg", code)

    def _handler_chejan_data(self, code, real_type, data):
        print("OnReceiveChejanData", code)

    def _handler_trc_data(self, code, real_type, data):
        print("OnReceiveTrCondition", code)

    def GetCommRealData(self, code, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid)
        return data


class Worker(QThread):
    threadEvent = pyqtSignal(int)

    def __init__(self, stat, parent=None):
        super().__init__()
        self.stat = stat
        self.parent = parent
        self.isRun = False

    def run(self):
        if self.stat == 1:
            self.parent.init_socket()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()