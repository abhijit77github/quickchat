from ..models.auth_model import UserDb
from ..dependencies import Getdb

class UserUtl():
    def __init__(self, db: Getdb) -> None:
        self.db = db
        self.data = db.read_data()

    def get_users(self):
        return self.data.get('users')
    
    def get_user_by_mail(self, mail: str):
        users = self.get_users()
        if users:
            for usr in users:
                if usr.get('mail') == mail:
                    return UserDb(mail=usr.get('mail'), hashed_pass=usr.get('hashed_pass'))
            return False
        
    def add_user(self, usr: UserDb):
        if self.data.get('users'):
            self.data['users'].append(usr.model_dump())
        else:
            self.data['users'] = [usr.model_dump()]
        self.db.write_data(self.data)