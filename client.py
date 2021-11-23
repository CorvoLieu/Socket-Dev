import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print("[CONECTED] Succesfully connected")

    connected = True
    while connected:
        msg = input()

        if msg == DISCONECT_MESSAGE:
            connected = False
            
        client.send(msg.encode(FORMAT))

    client.close()

if __name__ == "__main__":
    main()