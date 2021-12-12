from contact import Contact

import socket
import os
import threading
import xml.etree.ElementTree as ET
import pickle

#Constant Information
IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

#All command
COMMAND = { 
    0: "!DISCONNECT",
    1: "!DISPLAY_LIST",
}

#Load phonebook and contact
phonebook = ET.parse('phonebook.xml')  #Open file
contact = phonebook.findall('contact') #Open as tree

#Make list contact from tree
def compileContactList() -> bytes:
    ls = []
    for c in contact:
        ls.append(compileFromTree(c))

    return ls

#Find by name
def findByName(name: str):
    result = []
    for c in contact:
        if c.find('name').text == name:
            result.append(compileFromTree(c))
    return result

#Find by phone
def findByPhone(phone: str):
    result = []
    for c in contact:
        if c.find('phone').text == phone:
            result.append(compileFromTree(c))
    return result

#Find by email
def findByEmail(email: str):
    result = []
    for c in contact:
        if c.find('email').text == email:
            result.append(compileFromTree(c))
    return result

#Find contact and return the contact
def findContact(msg: str):
    foundContacts = []

    if msg[6:10] == 'NAME':
        foundContacts = findByName(msg[11:])
    elif msg[6:10] == 'NUMB':
        foundContacts = findByPhone(msg[11:])
    elif msg[6:10] == 'MAIL':
        foundContacts = findByEmail(msg[11:])

    #Check return information
    if foundContacts:
        result = foundContacts
    else:
        result = 0

    return result

#Create a contact from tree Element
def compileFromTree(info: ET.Element) -> Contact:
    file = open(f"photo\\{info.attrib['id']}.jpg", 'rb')
    data = file.read()
    return Contact(info.find('name').text, info.attrib['id'], info.find('phone').text, info.find('email').text, data)

# Hoat dong/code chinh trong phan nay
def handle_client(clientSocket, clientAddr):
    print(f"[CONNECTION] {clientAddr} connected.")

    connected = True
    while connected:
        msg = clientSocket.recv(SIZE).decode(FORMAT)
        if not msg:
            continue

        if msg == COMMAND[0]:
            connected = False
            continue
        elif msg == COMMAND[1]:
            result = compileContactList()
        elif msg[1:5] == 'FIND':
            result = findContact(msg)
        else:
            print(f'[{clientAddr}] Unknown message: {msg}')
            continue
            
        respond = pickle.dumps(result)
        respondSize = len(respond)
        
        clientSocket.send(str(respondSize).encode(FORMAT))
        clientSocket.send(respond)

    clientSocket.close()
    print(f"[DISCONNECT] {clientAddr} Disconnected.")


def main():
    os.system('cls')
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
