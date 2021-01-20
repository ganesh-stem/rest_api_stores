# Session 5, Lecture 8. Retriving our item resourses from a database

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister # which is our resource
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# This tells us that SQLALCHEMY DATABASE is going to live at the
# root folder of our project.  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# In order to know when an object has changed but not been saved
# to the database, the extension flask sqlalchemy was tracking 
# every change that we made to the sqlalchemy session and that
# took some resources. Here we are turning it off because sqlalchemy
# itself, the main library, has it's own modification tracker which 
# is a bit better. So this turn off the flask SQLAlchemy modification
# tracker. It does not turn off the SQLAlchemy tracker. SO this is
# changing the extensions behaviour and not the underlying SQLAlchemy
# behaviour.  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# This is a decorator that is going to affect the method below it 
# and it's going to run that method before the first request into 
# this app.

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# the __main__ means the name of the file
if __name__ == '__main__':
    # There is this circular imports. Our ItemModel is going to
    # import db as well. If we import db at the top, and we are
    # also going to import the models at the top, when we import
    # the model, the model is going to import the db and the db is
    # going to be here in the app. 
    from db import db
    db.init_app(app)
    app.run(port=5000, debug =  True)