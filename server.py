import socket
from _thread import *
import pickle
from game import Game

print("................")

server = "192.168.68.100" # My IP
port = 4444 # Free port
server_address = (server, port)

listenning_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    listenning_sock.bind(server_address)
    print("Server binded")

except socket.error as e:
    str(e)

listenning_sock.listen()
print("Server started -> Waiting to a connection")

connected = set()
games = {}
idCount = 0

def ThreadedClient(conn, playerNum, gameId):
    global idCount
    conn.send(str.encode(str(playerNum)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.ResetWent()
                    elif data != "get":
                        game.Play(playerNum, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    client_sock, client_address = listenning_sock.accept()
    print("Connected to: ", client_address)

    idCount += 1
    playerNum = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        playerNum = 1

    start_new_thread(ThreadedClient, (client_sock, playerNum, gameId))
