from uuid import uuid4
import uuid

class Tok():
    def __init__(self) -> None:
        self.tok = str(uuid4())
    def get_token(self):
        return self.tok
    def new_token(self):
        self.tok = str(uuid4())
        return self.tok
    def __eq__(self, o: object) -> bool:
        if isinstance(o, str) and self.tok == o:
            return True