import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
DISCONECT_MESSAGE = "!DISCONNECT"

# Hoat dong/code chinh trong phan nay
def handle_client(conn, addr):
    print(f"[CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)

        if msg == DISCONECT_MESSAGE:
            connected = False
            continue
            
        print(f"[{addr}] {msg}")
    
    conn.close()
    print(f"[DISCONNECT] {addr} Disconnected.")


def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Waiting for client")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args=(conn, addr))
        thread.start()

        print(f"[CONNECTION] Active connection: {threading.active_count() - 1}.")
        

if __name__ == "__main__":
    main()