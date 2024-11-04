import os
import uuid

class Registration():
    def __init__(self, path) -> None:
        self.path = os.path.join(path, "config.bin")
        self.__init()

    def __repr__(self) -> str:
        return (f"Register({str(self.id)}, {self.__inToBool(self.exfilComplete)})")

    def __init(self):
        fileExists = os.path.isfile(self.path)
        if(fileExists):
            _size = os.path.getsize(self.path)
            with open(self.path, "rb") as p:
                options = p.read(_size)
                o_exfilComplete = options[0:1:1]
                self.exfilComplete = int.from_bytes(o_exfilComplete, "big")
                self.id = uuid.UUID(bytes=options[1:17:1])
        else:
            v = 0
            self.exfilComplete = v 
            self.id = uuid.uuid4()
            self.__writeIndicator(self.exfilComplete, self.id)


    def __writeIndicator(self, state, id):
        b_state = state.to_bytes(1, "big")
        with open(self.path, "ab+") as f:
            f.write(b_state)
            f.write(id.bytes)


    def __inToBool(self, value):
        result = False
        if(value == 1):
            result = True
        return result