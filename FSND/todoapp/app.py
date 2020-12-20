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


#We're defaulting the homepage to display the todo items of list#1 => list_id=1
@app.route ('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    lists = TodoList.query.all()
    active_list = TodoList.query.get(list_id) # to grap the active list --> used in todos title
    todos = Todo.query.filter_by(list_id=  list_id).order_by('id').all()
    return render_template('index.html', lists=lists, todos=todos, active_list=active_list)


@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)
        
        db.session.delete(list)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})

        
@app.route('/lists/<list_id>/set-completed', methods=['POST'])
# Aim of this is to set the todos items all as completed as soon as the parent TodoList is marked as completed
def set_completed_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            todo.completed = True
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return '', 200


@app.route('/todos/create', methods= ['POST'])
def create_todo():
    error= False
    body= {}
    #fetch json body from the request. Notice, in index.html (body: JSON.stringify) was a dictionary
    description =  request.get_json()['description']

    #implement try except blocks in order to aviod implicit commit when closing the connection if something went wrong!
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, completed=False, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['complete'] = todo.completed
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
        abort(500)

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

#used to run the app from terminal with the following command: $ FLASK_APP=app.py FLASK_DEBUG=true flask run
# However, the below is more convenient as it has same parameters like the above command and you just need to run it as: $ python app.py
if __name__ == '__main__':
    app.run(debug=True)