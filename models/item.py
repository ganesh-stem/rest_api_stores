# internal reperesentation the item
# We are going to import the db and then both the user
# and the item model are going to extend db.model and 
# what that's going to do is to tell the sqlalchemy entity
# that these classes ( the ItemModel and UserModel in user.py)
# are things that we are going to be saving in a database 
# and retrieving from a database. So it's going to create a
# map between the database and these objects 
from db import db

class ItemModel(db.Model):
    
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    score_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # It sees that we have a store id and therefore we can find the store 
    # in the database that matches this store id. Now every ItemModel has
    # a property store which matches the store_id.
    store = db.relationship('StoreModel')

    # as ItemModel is a internal repersentations so it also 
    # has to contain the properties of an item as object 
    # properties. This values mentioned below are going to 
    # be putted in the database. Now create a add_argument
    # of store_id
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}
    
    # This method should still be a class method because it is going to
    # return an object of ItemModel as opposed to a dictionary.
    @classmethod
    def find_by_name(cls, name):
        # query is defined in sqlalchemy and comes from db.Model
        # to get the first element we use id = 1, or filter_by()
        # multiple times,or first(). As this is a class model
        # we could use cls. 
        return cls.query.filter_by(name=name).first()

    # save_to_db() = insert()
    def save_to_db(self):
        # SQLAlchemy can directly translate from object to row in
        # a database, so we don't need to tell it which row to insert
        # in a database. We just have to tell it to insert this object 
        # into the database. The session is a collecton of ojects that
        # we are going to write in the database. We can add multiple objects
        # to the session and then write them all at once, and that's more
        # efficient but in this case because we are only inserting one
        # object and we are just adding and committing straight after. 
        # when we retrieve an object from a database that has a particular 
        # id then we can change the object's name and all we have to do is 
        # to add it to the session and commit it again and sqlalchemy will
        # do an update instead of an insert. So this session is used for both
        # for insert and update.
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
         db.session.delete(self)
         db.session.commit()