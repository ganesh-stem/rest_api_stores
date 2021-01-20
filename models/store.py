from db import db

class StoreModel(db.Model):
    
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    # it is many-to-one relationship. There could be many items 
    # with the same store id. items is the list of items models.
    # To not to create a new object for each new item that matches
    # the store id, we use lazy='dynamic'.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # When we use lazy dynamic, self.items no longer is a list
        # of items, now it is a query builder that has the ability
        # to look into the items table then we can use .all to 
        # retrieve all of the items in that table. Which means that
        # until we call the json method, we are not looking into the
        # table, which means that creating stores is very simple.
        # However, it also means that every time, we call the json 
        # method we have to go into the table, so then it is going 
        # to be slower and what that means is that we create a store
        # so we load up all the items and can call the json method
        # many times for free, esentially. If we use lazy dynamic,
        # every time we call the json method, we have to go into the
        # table, so then that is slower. 
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # save_to_db() = insert()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
         db.session.delete(self)
         db.session.commit()