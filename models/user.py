import sqlite3
from db import db


# This class is an API and security.py uses this interface to communicate
# with the user and the database. in the case of mobile and web apps, they 
# may use our rest API to communicate with a database and store items and 
# users.  
class UserModel(db.Model):
    # To tell sqlalchemy that whether these table is going to
    # be stored. 
    __tablename__ = 'users'

    # the id is a primary key as defined, which means that it is 
    # auto-incrementing. When we insert a new row into the database
    # , the sql engine we use, the sqlite in our case, will automatically
    # assign an id for us and when we create an object through the sql
    # alchemy, the id is given to us as well. So SQLAchemy would give us
    # the self.id, but when we create the object, we don't have to specify
    # the id because it is automaticallu generated. So it doesn't make sense
    # for us to give an id there. If we don't want an auto-incrementing id
    # then we could assign an id.  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()