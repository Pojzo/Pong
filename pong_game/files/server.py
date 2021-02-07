import socket
import threading
import game as pong_game
import pygame
import pickle
import time
from datetime import datetime

HEADER = 16
PORT = 5050
# get ip of the computer by name
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
INITIATION_MESSAGE = "!INITIATE"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # family, type
server.bind(ADDR)


def receive(conn):
    message = conn.recv(HEADER)
    message_len = message.decode(FORMAT)
    if message_len:
        message = conn.recv(int(message_len))
        message = pickle.loads(message)
        return message

    return None


def initiate(conn):
    if receive(conn) == INITIATION_MESSAGE:
        return True

    return False


def send(conn, message):
    pickled_message = pickle.dumps(message)
    message_bytes = pickled_message
    header_len = str(len(message_bytes)).encode(FORMAT)
    header_len += b' ' * (HEADER - len(header_len))#
    conn.send(header_len)
    conn.send(pickled_message)

game_object = None
def handle_client(conn, addr):
    send(conn, INITIATION_MESSAGE)
    while not initiate(conn):
        pass

    print('[CONNECTION UPDATE] Received initiation message from the client')
    global game_object
    game_object = pong_game.Game()
    game_thread = threading.Thread(target=run_game)
    game_thread.start()

    connected = True
    while connected:

        game_info = {
            'player_y' : game_object.paddle1.y,
            'enemy_y' : game_object.paddle2.y,
            'ball_pos' : (game_object.b.x, game_object.b.y)
        }
        message = receive(conn)
        if not message is None:
            if message == DISCONNECT_MESSAGE:
                connected = False
            else:
                #print(f'[INCOMING MESSAGE] {message}')
                cur_time = datetime.now()
                send(conn, game_info)

    print('[CONNECTION UPDATE] Client has disconnected from the server')
    conn.close()

count = 0
def run_game():
    while game_object.running:
        global count
        print(count)
        count += 1
        global game_object
        game_object.run()

pygame.quit()


def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 2}')


print('[STARTING] server is starting')
start()
