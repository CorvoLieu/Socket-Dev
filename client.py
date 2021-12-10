import pickle
import socket
import os
import time
import xml.etree.ElementTree as ET
from contact import Contact

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024 * 5

COMMAND = {
    0: "!DISCONNECT",
    1: "!DISPLAY_LIST",
    2: "!FIND_NAME_",
    3: "!FIND_NUMB_",
    4: "!FIND_MAIL_",
    5: "!LOAD_PHOTO"
}

def failConnect():
    pass

#In thong tin cua mot ng
def displayContact(c: Contact) -> None:
    print(f"Name: {c.getName()}")
    print(f"ID: {c.getID()}")
    print(f"Phone: {c.getPhone()}")
    print(f"Email: {c.getEmail()}")

#In thong tin toan bo danh ba
def displayPhoneBook(ls: list) -> None:
    print("----------------------------")
    for c in ls:
        displayContact(c)
        print("----------------------------")

#Save photo of all contact in phonebook
def savePhoneBookPhoto(lst: list):
    for contact in lst:
        saveContactPhoto(contact)

#Save photo of a contact in phonebook
def saveContactPhoto(contact: Contact):
    photoFile = open(f'client\\{contact.getID()}.jpg', 'wb')
    photoFile.write(contact.getPic())
    photoFile.close()

#Use with COMMAND dic: COMMAND[n]
def menu():
    while True:
        print("\tMenu\t")
        print("1. Display the phonebook")
        print("2. Find a contact")
        print("0. Disconnect")

        print("Your input: ", end = '')
        n = input()
        if (int(n) < 0 or int(n) > 2):
            print("!Unrecognize input, please try again!")
            continue
        elif int(n) == 2:
            print("\tFinding By:\t")
            print("1. Name")
            print("2. Phone Number")
            print("3. Email")
            print("0. Back")
            while True:
                print("Your input: ", end = '')
                m = input()
                if (int(m) < 0 or int(m) > 3):
                    print("!Unrecognize input, please try again!")
                    continue
                elif int(m) == 0:
                    break
                else:
                    print("Enter finding information: ", end = '')
                    info = input()
                    os.system('cls')
                    return int(n) + int(m) - 1, info
            os.system('cls')
            continue
        else:
            os.system('cls')
            return n, ''

#Hoat dong chinh trong phan nay
def main():
    os.system('cls')
    appRunning = True
    while(appRunning):
        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Connecting...')
            serverSocket.connect(ADDR)

            print("[CONNECTED] Succesfully connected")

            connected = True
            while connected:
                cmd, info = menu()
                msg = COMMAND[int(cmd)] + info

                if msg == COMMAND[0]:
                    connected = False
                    serverSocket.send(msg.encode(FORMAT))
                    continue

                serverSocket.send(msg.encode(FORMAT))

                dataLen = serverSocket.recv(SIZE).decode(FORMAT)
                fullData = serverSocket.recv(int(dataLen))

                if int(cmd) == 1:
                    ls = pickle.loads(fullData)
                    displayPhoneBook(ls)
                    savePhoneBookPhoto(ls)
                elif int(cmd) >= 2 and int(cmd) <= 4:
                    foundContact = pickle.loads(fullData)
                    if(foundContact == 0):
                        print(f'Cannot find {info} in the contact.')
                    else:
                        displayContact(foundContact)
                        saveContactPhoto(foundContact)

                        

                print("Enter to continue...")
                input()
                os.system('cls')

            serverSocket.close()
            appRunning = False
        except socket.error as msg:
            print(f'Connection error: {msg}')
            print('Reconnect in 5s')
            time.sleep(5)
            os.system('cls')

if __name__ == "__main__":
    main()