from flask import Flask, render_template, request, jsonify
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect


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


@app.route('/todos/create', methods= ['POST'])
def create_todo():
    #fetch json body from the request. Notice, in index.html (body: JSON.stringify) was a dictionary
    description =  request.get_json()['description']

    #Now use the above description variable to create a new todo record in our database
    #step1: use Todo class to create a column description from our variable description
    todo = Todo(description= description)
    #step2: add that column to our database - putting it in the pending stage
    db.session.add(todo)
    #step3: commit that change in order to take effect in the database
    db.session.commit()
    
    # Return useful json object to the index.html view 
    return jsonify({
        'description': todo.description
    })
