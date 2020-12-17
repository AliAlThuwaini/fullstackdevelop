from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#connect to db: Note: you need to create the db 'todoapp' manually through psql before running this app (Just emplty db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ali:123@localhost:5432/todoapp'
db = SQLAlchemy(app)



class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable= False)
    
    # define dunder repr method
    def __repr__(self):
        return f'<Todo: {self.id}, desc: {self.description}>'

db.create_all()


@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all())
