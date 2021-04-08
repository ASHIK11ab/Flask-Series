from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(20), nullable=False)
  message = db.Column(db.String(200), nullable=False)
  status = db.Column(db.String(10), nullable=True, default="pending")

def get_todo(todo_id):
  """ Returns a todo.

    :param todo_id: todo id of the todo to be returned
    :return: todo object which contains information about the todo
    :rtype: todo object
  """

  return Todo.query.filter(Todo.id == todo_id).first()

def get_pending_todos():
  """ Returns all pending todos.

    :return: a list of todo objects whose status is pending
    :rtype: list
  """

  return Todo.query.filter(Todo.status == 'pending').all()

def get_completed_todos():
  """ Returns all completed todos.

    :return: a list of todo objects whose status is completed
    :rtype: list
  """

  return Todo.query.filter(Todo.status == 'completed').all()
