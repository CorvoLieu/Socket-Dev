import socket
import threading
from contact import Contact

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"

COMMAND = { 
    0: "!DISCONNECT",
    1: "!DISPLAY_LIST",
    2: "!FIND_NAME_",
    3: "!FIND_NUMB_",
    4: "!FIND_MAIL_"
}

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

#Use with COMMAND dic: COMMAND[n]
def menu() -> int and str:
    print("\tMenu\t")
    print("1. Display the phonebook")
    print("2. Find a contact")
    print("0. Disconnect")

    while True:
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
                    return int(n) + int(m) - 1, info
            continue
        else:
            return n, ''
    

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print("[CONECTED] Succesfully connected")

    connected = True
    while connected:
        cmd, info = menu()
        msg = COMMAND[int(cmd)] + info

        if msg == DISCONECT_MESSAGE:
            connected = False
            
        client.send(msg.encode(FORMAT))

    client.close()

if __name__ == "__main__":
    main()