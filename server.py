import pickle
import socket
from _thread import start_new_thread

from game import Game

server = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Ждем подключения, сервер запустился")

games = {}
id_count = 0


def threaded_client(conn, p, game_id):
    global id_count
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:

                    if data == "reset":
                        game.reset_went()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Соединение потеряно")
    try:
        del games[game_id]
        print("Закрытие игры", game_id)
    except:
        pass
    id_count -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Подключение:", addr)

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 3
    if id_count % 3 == 1:
        games[game_id] = Game(game_id)
        print("Создание новой игры...")
    elif id_count % 3 == 2:
        p = 1
    else:
        games[game_id].ready = True
        p = 2

    start_new_thread(threaded_client, (conn, p, game_id))
