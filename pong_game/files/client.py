import socket
import game as pong_game
import pygame
import pickle
from datetime import datetime
import threading


HEADER = 16
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.100.19'
ADDR = (SERVER, PORT)
INITIATION_MESSAGE = '!INITIATE'


def receive(conn):
    message_len = conn.recv(HEADER)
    message_len = message_len.decode(FORMAT)


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

def run_game():
    while game_object.running:
        global game_object
        game_object.run()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print('[CONNECTION] Connected to server')

while not initiate(client):
    pass

print('[CONNECTION UPDATE] Received initiation message')
send(client, INITIATION_MESSAGE)
connected = True
cur_time = datetime.now()
send(client, cur_time)
game_object = pong_game.Game()
game_object.local = False
thread = threading.Thread(target=run_game)
thread.start()

while connected:
    try:
        message = receive(client)
        if not message is None:
            if message == DISCONNECT_MESSAGE:
                connected = False
                break
            else:
                #print(f'[INCOMING MESSAGE] {message}')
                game_object.paddle1.y = message['player_y']
                game_object.paddle2.y = message['enemy_y']
                game_object.b.x, game_object.ball_y = message['ball_pos']
                cur_time = datetime.now()
                send(client, cur_time)
    except ConnectionResetError:
        connected = False

print('[CONNECTION UPDATE] Disconnecting from the server')


# while not initiated:
#     print(initiated)
#     receive()

# message = receive()


# game = pong_game.Game()
# while game.running:
#     message = receive()
#     game.local = False
#     game.run()

# pygame.quit()
