from flask import Flask, render_template, request, redirect
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_user:12345@localhost:5432/todo_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=["GET", "POST"])
def home():
  if request.method == "GET":
    todos = get_pending_todos()
    return render_template('index.html', todos = todos, cnt = len(todos))
  title = request.form.get('title')
  message = request.form.get('message')
  todo = Todo(title=title, message=message)
  db.session.add(todo)
  db.session.commit()
  return redirect('/')

@app.route('/todos/complete/<int:todo_id>')
def complete_todo(todo_id):
  todo = get_todo(todo_id)
  if todo is None:
    return "<h1>Invalid todo id</h1>"
  todo.status = 'completed'
  db.session.commit()
  return redirect('/')

@app.route('/todos/delete/<int:todo_id>')
def delete_todo(todo_id):
  todo = get_todo(todo_id)
  if todo is None:
    return "<h1>Invalid todo id</h1>"
  db.session.delete(todo)
  db.session.commit()
  return redirect('/')

@app.route('/todos/completed')
def completed_todos():
  todos = get_completed_todos()
  return render_template('completed.html', todos = todos, cnt = len(todos))

@app.route('/todos/<int:todo_id>')
def todo(todo_id):
  todo = get_todo(todo_id)
  if todo is None:
    return "<h1>Invalid todo id</h1>"
  return render_template('todo.html', todo=todo)


if __name__ == "__main__":
  with app.app_context():
    app.run()