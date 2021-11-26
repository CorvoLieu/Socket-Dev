import socket
import threading
import xml.etree.ElementTree as ET

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
DISCONECT_MESSAGE = "!DISCONNECT"

phonebook = ET.parse('phonebook.xml')
contact = phonebook.findall('contact')

#In thong tin cua mot ng
def displayContact(c: ET.Element) -> None:
    print(f"Name: {c.find('name').text}")
    print(f"ID: {c.attrib['id']}")
    print(f"Phone: {c.find('phone').text}")
    print(f"Email: {c.find('email').text}")

#In thong tin toan bo danh ba
def displayPhoneBook() -> None:
    print("----------------------------")
    for c in contact:
        displayContact(c)
        print("----------------------------")

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