from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self,id,username,email,image,password):
        self.id=id
        self.username=username
        self.email=email
        self.image=image
        self.password=password

    @classmethod
    def checkPassword(cls,hashed_password,password):
        return check_password_hash(hashed_password,password)
    


print('User funciona')