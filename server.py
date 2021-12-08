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
    for c in contact:
        if c.find('name').text == name:
            return c
    return 0

#Find by phone
def findByPhone(phone: str):
    for c in contact:
        if c.find('phone').text == phone:
            return c
    return 0

#Find by email
def findByEmail(email: str):
    for c in contact:
        if c.find('email').text == email:
            return c
    return 0

#Find contact and return the contact
#isFound return true if the contact is found
def findContact(msg: str):

    if msg[6:10] == 'NAME':
        foundContact = findByName(msg[11:])
    elif msg[6:10] == 'NUMB':
        foundContact = findByPhone(msg[11:])
    elif msg[6:10] == 'MAIL':
        foundContact = findByEmail(msg[11:])

    #Check return information
    if foundContact != 0:
        result = compileFromTree(foundContact)    
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
        isFound = False

        if msg == COMMAND[0]:
            connected = False
            continue
        elif msg == COMMAND[1]:
            result = compileContactList()
        elif msg[1:5] == 'FIND':
            result = findContact(msg)
            
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
