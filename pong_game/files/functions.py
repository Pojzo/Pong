import socket
import game as pong_game
import pygame
import pickle
from datetime import datetime
import threading


HEADER = 16
PORT = 10000
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.100.19'
ADDR = (SERVER, PORT)
INITIATION_MESSAGE = '!INITIATE'

def send(conn, message):
    pickled_message = pickle.dumps(message)
    message_bytes = pickled_message
    header_len = str(len(message_bytes)).encode(FORMAT)
    header_len += b' ' * (HEADER - len(header_len))
    conn.send(header_len)
    conn.send(pickled_message)

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

