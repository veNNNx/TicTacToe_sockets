import socket
from _thread import *
import pickle
from game import Game

server = "IP ADDRESS"
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Server started...")

connected = set()
games = {}
board_id = 0


def threaded_client(conn, p, game_id):
    global board_id
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
                        game.reset()
                        print(f'[Game {game_id}] Reset Board, now starting client {game.who_started}')
                    elif data != "update":
                        game.save_move(p, data)
                        print(f'[Game {game_id}] Client {p}, btn.id {data}')

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    board_id -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    board_id += 1
    p = 0
    game_id = (board_id - 1)//2

    if board_id % 2 == 1:
        games[game_id] = Game(game_id)
        print(f"[Game {game_id}] New game")
    else:
        games[game_id].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, game_id))