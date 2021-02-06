import socket
import game as pong_game
import pygame
import pickle

def send(msg):
    message = pickle.dumps(msg)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receive():
    message_len = client.recv(HEADER).decode(FORMAT)
    if message_len:

        message_len = int(message_len)
        #msg = pickle.load(client.recv(message_len))
        msg = client.recv(message_len)

        if msg == INITIATION_MESSAGE:
            global initiated
            initiated = True
            print('[INCOMING MESSAGE] Received initiation message' )
        elif msg == DISCONNECT_MESSAGE:
            alive = False
            print('[INCOMING MESSAGE] Disconnecting from server')
        else:
            return msg




HEADER = 16
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.100.15'
ADDR = (SERVER, PORT)
INITIATION_MESSAGE = '!INITIATE'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print('[CONNECTION] Connected to server')

send(INITIATION_MESSAGE)

initiated = False
alive = True

msg = client.recv(1024)
print(pickle.loads(msg))

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


