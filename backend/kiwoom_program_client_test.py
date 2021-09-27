import socket
import json
import ast

host = "127.0.0.1"
port = 4000

if __name__ == '__main__':
    msg = dict()
    msg['symbol'] = "005930"
    msg['method'] = "get_hoga"
    byte_msg = json.dumps(msg, indent=2).encode('utf-8')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    client_socket.sendall(byte_msg)

    cnt = 0
    while True:
        if cnt > 10 :
            # client_socket.sendall("0".encode())
            break
        cnt += 1

        rec = client_socket.recv(128)
        rec_decode = ast.literal_eval(rec.decode('utf-8'))
        print("받은 데이터1는 \"", rec_decode, "\" 입니다.", sep="")
        rec = client_socket.recv(128)
        rec_decode = ast.literal_eval(rec.decode('utf-8'))
        print("받은 데이터2는 \"", rec_decode, "\" 입니다.", sep="")

    client_socket.close()
    print("접속을 종료합니다.")