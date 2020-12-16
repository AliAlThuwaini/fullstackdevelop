from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #This is to silent the overhead warning when running the app in the python interaction mode

#connect to our database from our flask app
#The way to connect through sqlalchamy is as follows:
#dialect://username:pw@host:port/dbname     Example:
#postgresql://myuser:mypassword@localhost:5432/mydatabaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ali:123@localhost:5432/example'
#The above URL is theoritically OK but it gave me the following error: 'sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) fe_sendauth: no password supplied'. I read in Stackoverflow to remove the local host so that it tells psycopg2 to use Unix-domain sockets. read: https://stackoverflow.com/questions/23839656/sqlalchemy-no-password-supplied-error
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///example'

#using sqlalchamy as the medium to interact with our db
db = SQLAlchemy(app)

class Persons(db.Model): #Person(db.Model): inherits from db.Model. By inheriting, we map from our classes to tables via SQLAlchamy ORM.
    __tablename__ = 'persons' #This is optional to control table name. sqlalchemy will automatically grap your class name and name your table the same with lowercase!
    id = db.Column(db.Integer, primary_key= True) # This is to bind your attribute (id) to a cloumn in the db and specify the column specs (primary, data type ... etc)
    name = db.Column(db.String(), nullable= False)

    # Customize the way the class prints its results as we import flask_hello_app in the interactive python. Before having the __repr__ function, the output of e.g. >>>Person.query.all() is: [<Person 1>]. However, after adding it like below the output became: <Person ID: 1, name: Amy>
    #   for the same query!
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(), nullable= False)

    def __repr__(self):
        return f'<User ID: {self.id}, name: {self.name}>'

db.create_all() # This looks at the above table/s and create them in our db in case they don't exist. if exists, nothing is done. This is important as we run our flask app multilple times.


@app.route('/')
def index():
    person= Persons.query.first() # This gives the first record in the table person
    return 'Hello '+ person.name
    #return 'Hello World!'


# if __name__ == "__main__":
#     app.run()