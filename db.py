from flask_sqlalchemy import SQLAlchemy

# Here we got an object which is sqlalchemy and that is a thing 
# going to link to our flask app and it's going to look at all
# of the the objects that we tell it to and then it's going to
# allow us to map those objects to rows in a database. For example,
# when we create an item model object that has a column name and
# a column price. It's going to allows us to easily put that object
# into database. Naturally, putting an object into database, all that 
# is saving the object's properties into the database and that's what
# sqlalchemy excels at.  
db = SQLAlchemy()