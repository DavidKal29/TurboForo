from models.entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():

    @classmethod
    def login(cls,db,user):
        try:
            cursor=db.connection.cursor()
            sql='SELECT * FROM users WHERE email=%s'
            values=(user.email,)

            cursor.execute(sql,values)
            row=cursor.fetchone()

            if row:
                id=row[0]
                username=row[1]
                email=row[2]
                image=row[3]
                password=User.checkPassword(row[4],user.password)

                logged_user=User(id,username,email,image,password)

                return logged_user
            else:
                return None
        
        
        except Exception as error:
            print(error)
            return None
        
    @classmethod
    def register(cls,db,user):
        try:
            cursor=db.connection.cursor()
            sql='INSERT INTO users (username,email,image,password) VALUES (%s,%s,%s,%s)'
            values=(user.username,user.email,user.image,generate_password_hash(user.password))

            cursor.execute(sql,values)
            db.connection.commit()

            user=User(0,'',user.email,'',user.password)

            sql='SELECT * FROM users WHERE email=%s'
            values=(user.email,)

            cursor.execute(sql,values)
            row=cursor.fetchone()

            if row:
                id=row[0]
                username=row[1]
                email=row[2]
                image=row[3]
                password=User.checkPassword(row[4],user.password)

                logged_user=User(id,username,email,image,password)

                return logged_user
            else:
                return None

        except Exception as error:
            print(error)
            return None
        
    @classmethod
    def get_by_id(cls,db,id):
        try:
            cursor=db.connection.cursor()
            sql='SELECT * FROM users WHERE id=%s'
            values=(id,)

            cursor.execute(sql,values)

            row=cursor.fetchone()
            if row:
                id=row[0]
                username=row[1]
                email=row[2]
                image=row[3]
                password=None
                logged_user=User(id,username,email,image,password)

                return logged_user
            else:
                return None
        except Exception as error:
            print(error)
            return None



