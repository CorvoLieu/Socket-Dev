
from contact import Contact

import socket
import threading
import xml.etree.ElementTree as ET
import pickle


IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

COMMAND = { 
    0: "!DISCONNECT",
    1: "!DISPLAY_LIST",
}

phonebook = ET.parse('phonebook.xml')
contact = phonebook.findall('contact')

#Gui list contact
def sendContactList() -> list:
    pass

#Tim bang ten
def findByName(name: str):
    for c in contact:
        if c.find('name').text == name:
            return c
    return 0

#Tim bang phone
def findByPhone(phone: str):
    for c in contact:
        if c.find('phone').text == phone:
            return c
    return 0

#Tim bang email
def findByEmail(email: str):
    for c in contact:
        if c.find('email').text == email:
            return c
    return 0

def contactFromTree(info: ET.Element) -> Contact:
    return Contact(info.find('name').text, info.attrib[id], info.find('phone').text, info.find('email').text)

# Hoat dong/code chinh trong phan nay
def handle_client(conn, addr):
    print(f"[CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)

        if msg == COMMAND[0]:
            connected = False
            continue
        # elif msg == COMMAND[1]:
        #     sendContactList()
        # elif msg[1:4] == "FIND":
        #     pass

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
