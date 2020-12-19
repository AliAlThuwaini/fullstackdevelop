from flask import Flask, render_template, request, jsonify, abort, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
#importing sys module to display error if they exist
import sys
from flask_migrate import Migrate
from sqlalchemy.orm import backref


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#connect to db: Note: you need to create the db 'todoapp' manually through psql before running this app (Just emplty db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ali:123@localhost:5432/todoapp'
db = SQLAlchemy(app)

#Define our migrate. it has to link between our flask app and our sqlalchemy instance
migrate = Migrate(app, db)


#this is the child model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable= False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # referencing the parent table using foreign key logic
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False) #although by default is it not null becuase it references a primary key, but we wanted to be explicit!
    
    # define dunder repr method
    def __repr__(self):
        return f'<Todo: {self.id}, desc: {self.description}>'

#this is the parent model and it has one-to-many relationship with child model Todo above.
class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable= False)
    #setting up the relationship with child model Todo:
    #backref: this is a custom name referencing what the parent name should be! we set: backref= 'list' so that it will be Todo.list to refer to the parent list name
    todos = db.relationship('Todo', backref= 'list', lazy=True)



# As we're using flask-migrate to sync our models, we don't need to use db.create_all() anymore.
#db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.order_by('id').all())


@app.route('/todos/create', methods= ['POST'])
def create_todo():
    error= False
    body= {}
    #fetch json body from the request. Notice, in index.html (body: JSON.stringify) was a dictionary
    description =  request.get_json()['description']

    #implement try except blocks in order to aviod implicit commit when closing the connection if something went wrong!
    try:
        #Now use the above description variable to create a new todo record in our database
        #step1: use Todo class to create a column description from our variable description
        todo = Todo(description= description)
        #step2: add that column to our database - putting it in the pending stage
        db.session.add(todo)
        #step3: commit that change in order to take effect in the database
        db.session.commit()

        #body var was created so that we don't access todo.descritiopn in the return statement after closing the connection. If you try to return it after closing connection it raises an error because it is not bound anymore!
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if not error:           
        # Return useful json object to the index.html view 
        return jsonify(body)
    else:
        abort(400)

@app.route('/todos/<todo_id>/set-completed', methods= ['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/<todo_id>/delete', methods= ['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        print
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify({'success': True})

