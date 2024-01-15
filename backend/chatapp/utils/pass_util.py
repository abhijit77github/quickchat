
class PassUtil:
    def __init__(self) -> None:
        # set haslib context
        pass

    def hash_pass(self, password: str) -> str:
        return password + " -- hashed"
    
    def verify_pass(self, password:str, hash_pass: str)-> bool:
        return self.hash_pass(password) == hash_pass
            