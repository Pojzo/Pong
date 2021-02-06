import socket
import threading
import game as pong_game
import pygame
import pickle

HEADER = 16
PORT = 5050 
SERVER = socket.gethostbyname(socket.gethostname()) # get ip of the computer by name
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
INITIATION_MESSAGE = "!INITIATE"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # family, type
server.bind(ADDR)

def send(conn, msg):
    msg_length = len(msg.encode(FORMAT))
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(pickle.dumps(msg))


def handle_client(conn, addr):
    conn.send(pickle.dumps('Hello'))
    # print(f'[NEW CONNECTION] {addr} connected.')
    # initiated = False
    # while not initiated:
    #     message_len = conn.recv(HEADER).decode(FORMAT)
    #     while not message_len:
    #         message_len = conn.recv(HEADER).decode(FORMAT)

    #     message_len = int(message_len)
    #     msg = pickle.loads(conn.recv(message_len))
    #     if msg == INITIATION_MESSAGE:
    #         print('[INCOMING MESSAGE] Received initiation message')
    #         initiated = True
    
    # send(conn, INITIATION_MESSAGE)
    # send(conn, DISCONNECT_MESSAGE)

    # connected = True
    # while connected:
    #     message_len = conn.recv(HEADER).decode(FORMAT)
    #     if message_len:
        
    #         message_len = int(message_len)
    #         msg = conn.recv(message_len).decode(FORMAT)
    #         if msg == DISCONNECT_MESSAGE:
    #             connected = False

    #         conn.send('Received your message'.encode(FORMAT))  

    #         print(f"[{addr}] {msg}")

    # print(f'Disconnect from [{addr}]')
    # conn.close()

def run_game():
    game = pong_game.Game()
    while game.running:
        game.local = False
        game.run()

pygame.quit()

def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    game_thread = threading.Thread(target=run_game)
    game_thread.start()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 2}')


print('[STARTING] server is starting')
start()
