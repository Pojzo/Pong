import socket
import threading

HEADER = 16
PORT = 5050 
SERVER = socket.gethostbyname(socket.gethostname()) # get ip of the computer by name
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # family, type
server.bind(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    server.send(send_length)
    server.send(message)
    received_message = server.recv(2048).decode(FORMAT)
    print(f'{received_message}')

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        message_len = conn.recv(HEADER).decode(FORMAT)
        if message_len:
        
            message_len = int(message_len)
            msg = conn.recv(message_len).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            conn.send('Received your message'.encode(FORMAT))  

            print(f"[{addr}] {msg}")

    print(f'Disconnect from [{addr}]')
    conn.close()

def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


print('[STARTING] server is starting')
start()

