import socket
import threading
from datetime import datetime
from functions import send, receive, initiate

HEADER = 16
PORT = 10000
# get ip of the computer by name
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
INITIATION_MESSAGE = "!INITIATE"

def server_handle(server):
    server.bind(ADDR)
    server.listen()
    print(f'[SERVER UPDATE] Server is running and listening on port {PORT}')
    conn, addr = server.accept()
    print(f'[SERVER CONNECTION UPDATE] Connected to {addr}')
    print('[SERVER INFO] Waiting for initiation message')
    initiated = False
    while not initiated:
        initiated = initiate(conn)

    print(f'[SERVER CONNECTION UPDATE] Received initiation message from {addr}')

    connected = True
    while connected:
        message = receive(conn)
        if not message is None:
            if message == DISCONNECT_MESSAGE:
                connected = False
            else:
                cur_time = datetime.now()
                send(conn, cur_time)


    print(f'[SERVER CONNECTION UPDATE] {addr} disconnected')
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_thread = threading.Thread(target=server_handle, args=(server,))
server_thread.start()