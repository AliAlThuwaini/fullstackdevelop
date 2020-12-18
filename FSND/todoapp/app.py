from flask import Flask, render_template, request
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

# This route listen to request to create a new todo item and control that process
@app.route('/todos/create', methods= ['POST'])
def create_todo():
    #This assumes that the post request will come as a form and hence, we can use request.form to handle it.

    #This will get the the request input from field name=descrioption from the form in the index.html view and we default it to empty string in case there is not input.
    description =  request.form.get('description', '')

    #Now use the above description variable to create a new todo record in our database
    #step1: use Todo class to create a column description from our variable description
    todo = Todo(description= description)
    #step2: add that column to our database - putting it in the pending stage
    db.session.add(todo)
    #step3: commit that change in order to take effect in the database
    db.session.commit()
    
    #Now we want to go back to user, but what should we display? let's let the view to redirect to the index route and reshow the index page. index route will grap a fresh of all records in the todos table as a result of 
    # data = Todo.query.all()
    return redirect(url_for('index')) #index here is the function name of the handler used to listen to our index route 



@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all())
