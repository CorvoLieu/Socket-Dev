
class Contact:
    def __init__(self, name: str, id: str, phone: str, email: str, picData: bytes) -> None:
        self.name = name
        self.id = id
        self.phone = phone
        self.email = email
        self.picData = picData

    def getName(self) -> str:
        return self.name

    def getID(self) -> str:
        return self.id

    def getPhone(self) -> str:
        return self.phone

    def getEmail(self) -> str:
        return self.email

    def getPic(self) -> bytes:
        return self.picData