import socket
import threading
from bottle import route, run, get, post, request, redirect
from pyA20.gpio import gpio
from pyA20.gpio import port




HEADER = 64
PORT = 5050
SERVER = "192.168.40.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        relay = port.PA06

        gpio.init()
        gpio.setcfg(relay, gpio.OUTPUT)


        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg == "HIGH":
                gpio.output(relay.gpio.HIGH)

                print("Relay OPEN!")
            elif msg == "LOW":
                gpio.output(relay.gpio.LOW)
                print("Relay CLOSED!")

            print(f"[{addr}] {msg}")
            conn.send("OKEY!".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()