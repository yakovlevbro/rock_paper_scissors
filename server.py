import socket
from _thread import start_new_thread

server = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Ждем подключения, сервер запустился")


def threaded_client(conn, p):
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()
        except:
            break

    print("Соединение потеряно")
    conn.close()

p = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, p))
    p += 1
