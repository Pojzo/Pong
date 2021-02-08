import socket
import game as pong_game
import pygame
import pickle
from datetime import datetime
import threading
from functions import send, receive, initiate


HEADER = 16
PORT = 10000
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.100.19'
ADDR = (SERVER, PORT)
INITIATION_MESSAGE = '!INITIATE'

def client_handle(client):
    client.connect(ADDR)
    print('[CLIENT CONNECTION UPDATE] Connected to the server')
    initiated = False
    send(client, INITIATION_MESSAGE)
    connected = True
    message = INITIATION_MESSAGE
    while connected:
        if message == DISCONNECT_MESSAGE:
            connected = False
        else:
            response = "got ya"
            send(client, response)
            print(message)

        message = receive(client)
    print('[CLIENT CONNECTION UPDATE] Disconnecting from the server')
    client.close()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_thread = threading.Thread(target=client_handle, args=(client,))
client_thread.start()