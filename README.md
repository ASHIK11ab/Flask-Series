## Todo list application in Flask (Part II)

### Overview
- In this episode we are going to start from where we left in creating the Todo App.
- To see the YouTube demonstration of this tutorial [click here.](https://youtu.be/P1Gj-OK2oXg)
- If you wanted to see the part I of creating the Todo App [click here.](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part1)

<!-- | &emsp;&emsp;&emsp;Table of Contents |
| --- |
| 1. [**Creating our application**](#creating-our-application) |
| 2. [**Creating a layout file**](#creating-a-layout-file) |
| 3. [**Creating index.html**](#creating-index.html) |
| 4. [**Styling our elements**](#styling-our-elements) |
| 5. [**Final touch with JavaScript**](#final-touch-with-javascript) | -->

### Setting up the environment
- Download this [Pipfile.lock](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/Pipfile.lock) and install the necessary dependencies by running
  ```bash
    > pipenv sync
  ```
- This will install the dependencies from Pipfile.lock

### Note:
> - Since pipfile varies accross various operating systems. If you get into trouble installing the dependencies. Then,
> - Manually install the dependencies by running
>  ```bash
>   > pipenv install Flask Flask-SQLAlchemy psycopg2
>  ```
<br>

### Step by Step Guide
1. Lets start with the backend stuff.

2. Lets model a SQL table as a class using Flask-SQLAlchemy in [models.py](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-part2/models.py).

```python
  from flask_sqlalchemy import SQLAlchemy

  db = SQLAlchemy()

  class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), nullable=True, default="pending")
```
&emsp;&emsp;&emsp;&emsp;i. First we create a database object by saying 'db = SQLAlchemy()'.
&emsp;&emsp;&emsp;&emsp;ii. Then, we create a <kbd>class</kbd> called Todo which inherits from 'db.Model' class.<br>
&emsp;&emsp;&emsp;&emsp;iii. In our <kbd>class Todo</kbd> we have four columns namely 'id', 'title', 'message', 'status'.<br>

> The column 'status' has a default value of pending since all todos are pending at the time of creation.

3. Now we need to convert our <kbd>class</kbd> into a SQL table.

4. Now lets first setup a couple of configuration values for our application.
```python
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{usernaem}:{password}@localhost:5432/{database_name}'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

5. Now lets import everything from our models file into our app file and lets convert our classes into SQL tables.
```python
  from models import *

  db.init_app(app)

  @app.route('/')
  def home():
    db.create_all()
    return render_template('index.html')

  if __name__ == "__main__":
    with app.app_context():
      app.run()
```
> Since we are using the <kbd>init_app()</kbd> method to tie our application with our database object :<br>
> i. We need to run our application using our application's context.<br>
> ii. We can use the <kbd>create_all()</kbd> only inside a view function thats why we have added it in the index route.<br>
> iii. Inorder to create our tables, go to the index route in the browser and refresh the page.

6. Before going further, lets create a bunch of utility functions in [models.py](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/models.py)

```python
  def get_todo(todo_id):
    """ Returns a todo.

      :param todo_id: todo id of the todo to be returned
      :return: todo object which contains information about the todo
      :rtype: todo object
    """

    return Todo.query.filter(Todo.id == todo_id).first()
```
```python
  def get_pending_todos():
    """ Returns all pending todos.

      :return: a list of todo objects whose status is pending
      :rtype: list
    """

    return Todo.query.filter(Todo.status == 'pending').all()
```
```python
  def get_completed_todos():
    """ Returns all completed todos.

      :return: a list of todo objects whose status is completed
      :rtype: list
    """

    return Todo.query.filter(Todo.status == 'completed').all()

```

7. Now we need to get the form data in the backend and we need to add the todo to the database.
```python
  @app.route('/', methods=["GET", "POST"])
  def home():
    if request.method == "GET":
      return render_template('index.html')
    title = request.form.get('title')
    message = request.form.get('message')
    todo = Todo(title=title, message=message)
    db.session.add(todo)
    db.session.commit()
    return redirect('/')
```

8. Now when the user visits the index route we need to get all of the pending todos and pass it to our [index.html](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/templates/index.html)
```python
  @app.route('/', methods=["GET", "POST"])
  def home():
    if request.method == "GET":
      todos = get_pending_todos()
      return render_template('index.html', todos = todos, cnt = len(todos))
```

9. Consolidating our index route should look like this now.
```python
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
```

10. Now lets add the pending todos in our index.html page.

```html
  <div class="todo-container">
    <h2>{{ cnt }} Pending todos</h2>
    {% if cnt != 0 %}
      {% for todo in todos %}
        <div class="todo-card">
          <div class="todo-content">
            <a href="{{ url_for('todo', todo_id=todo.id) }}" target="_blank">{{ todo.title }}</a>
          </div>
          <div class="btn-box">
            <a id="complete" type="button" href="{{ url_for('complete_todo', todo_id=todo.id) }}">
              Mark as complete
            </a>
            <a id="delete" type="button" href="{{ url_for('delete_todo', todo_id=todo.id) }}">
              Delete todo
            </a>
          </div>
        </div>
      {% endfor %}
    {% endif %}
  </div>
```
&emsp;&emsp;&emsp;&emsp;i. If the number of todos is not equal to zero. Then, we loop through the todos and for each todo we display it as a card.<br>
&emsp;&emsp;&emsp;&emsp;ii. In each todo card we have two buttons one for marking todo as complete and another one for deleting a todo.<br>
&emsp;&emsp;&emsp;&emsp;iii. When user clicks on the todo title we display a detailed information of the todo in a another page.<br>
> We will create all these routes in a moment after styling the todo card.

11. Consolidatig, our index.html [should look like this](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/templates/index.html).

12. Now we need to style our todo card in 'index.css'.<br>
&emsp;&emsp;&emsp;&emsp;i. For the <kbd>.todo-container</kbd> lets display it as flex and with <kbd>flex-direction: column</kbd> to display all elements in a column. Lets also center the container by giving a width of 80% and with margin set to auto. 
```css
  .todo-container {
    margin-top: 2rem;
    width: 80%;
    margin: auto;
    display: flex;
    flex-direction: column;
  }
```
&emsp;&emsp;&emsp;&emsp;ii. Now, for the <kbd>.todo-card</kbd> lets display it as flex to display elements in <kbd>.todo-card</kbd> in a row.
```css
  .todo-card {
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 1.5rem;
    border: .8px solid #ddd;
    border-radius: 8px;
    margin-top: 1rem;
  }
```
&emsp;&emsp;&emsp;&emsp;iii. For the <kbd>.btn-box</kbd> which contains two buttons lets display it in column using <kbd>flex</kbd> and also lets do some basic styling on 'anchor tags'.
```css
  .todo-content a {
    text-decoration: none;
    font-size: 1.3rem;
  }

  .btn-box {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
  }

  .btn-box a {
    color: #fff;
    padding: .8rem;
    font-size: 1rem;
    text-decoration: none;
    margin-top: 10px;
    border-radius: 10px;
  }
```
&emsp;&emsp;&emsp;&emsp;iv. Lets give some background color to the buttons in <kbd>.btn-box</kbd>.
```css
  #complete {
    background-color: #00ff00;
  }

  #delete {
    background-color: #ff0000;
  }
```

13. Consolidatig, our index.css [should look like this](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/static/css/index.css).

14. Now we need to work on marking a todo as done and deleting a todo.

15. For marking a todo as done. Lets create a view function called <kbd>complete_todo(todo_id)</kbd> which takes a todo id as a parameter.
```python
  @app.route('/todos/complete/<int:todo_id>')
  def complete_todo(todo_id):
    todo = get_todo(todo_id)
    if todo is None:
      return "<h1>Invalid todo id</h1>"
    todo.status = 'completed'
    db.session.commit()
    return redirect('/')
```
&emsp;&emsp;&emsp;&emsp;i. The <kbd>\<int:todo_id\></kbd> is a int URL converter by which this route accepts a todo id of type integer which is passed as a parameter to its view function.<br>
&emsp;&emsp;&emsp;&emsp;ii. The reason to check <kbd>if the todo is None</kbd> is because if the user manually types the url we want to make sure that a todo with the given id actually existes.<br>
&emsp;&emsp;&emsp;&emsp;iii. Last, we change the status of the todo to completed and we commit our changes and we redirect user back to the index route.

16. Now we need to work on deleting a todo.
```python
  @app.route('/todos/delete/<int:todo_id>')
  def delete_todo(todo_id):
    todo = get_todo(todo_id)
    if todo is None:
      return "<h1>Invalid todo id</h1>"
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
```
&emsp;&emsp;&emsp;&emsp;i. Deleting a todo is almost similar to marking a todo as done. Instead of changing the status of the todo to completed we use <kbd>db.session.delete(todo)</kbd> method to delete a todo.<br>
&emsp;&emsp;&emsp;&emsp;ii. After deleting a todo we redirect users back to the index route.

17. Since, completing and deleting a todo is done. Now when the user clicks in the <kbd>complete</kbd> link in the navigation bar we need to list all of the completed todos.
```python
  @app.route('/todos/completed')
  def completed_todos():
    todos = get_completed_todos()
    return render_template('completed.html', todos = todos, cnt = len(todos))
```
&emsp;&emsp;&emsp;&emsp;i. In the <kbd>/todos/completed</kbd> route we get all of the completed todos and we pass it to [completed.html](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/templates/completed.html).

18. In completed.html we are going to display all of the todos as a card like we did for the pending todos except we will not have a button to mark a todo as done since the todo is aldready completed.
```html
  {% extends "layout.html" %}

  {% block title %}
    Completed todos
  {% endblock %}

  {% block body %}
    <div class="todo-container">
      <h2>{{ cnt }} Completed todos</h2>
      {% if cnt != 0 %}
        {% for todo in todos %}
          <div class="todo-card">
            <div class="todo-content">
              <a href="{{ url_for('todo', todo_id=todo.id) }}" target="_blank">{{ todo.title }}</a>
            </div>
            <div class="btn-box">
              <a id="delete" type="button" href="{{ url_for('delete_todo', todo_id=todo.id) }}">
                Delete todo
              </a>
            </div>
          </div>
        {% endfor %}
      {% endif %}
    </div>
  {% endblock %}
```

19. There is one last thing that we need to do. When a user clicks on the todo title we want to display a detailed information of the todo.
```python
  @app.route('/todos/<int:todo_id>')
  def todo(todo_id):
    todo = get_todo(todo_id)
    if todo is None:
      return "<h1>Invalid todo id</h1>"
    return render_template('todo.html', todo=todo)
```
&emsp;&emsp;&emsp;&emsp;i. After getting the todo id we make sure that the todo actually exists. If so, we pass it into [todo.html](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/templates/todo.html).

20. Consolidating our `app.py` [should look like this now](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2/app.py).

21. In <kbd>todo.html</kbd> we print the todo information as card which is centered in the window with some basic styling.
```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
      Todo #{{todo.id}}
    </title>
    <style>
      .todo-card {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 2rem;
        font-size: 1.2rem;
      }
    </style>
  </head>
  <body>
    <div class="todo-card">
      <h2>Todo #{{todo.id}}</h2>
      <p>
        <strong>Title: </strong>{{todo.title}}
      </p>
      <p>
        <strong>Message: </strong>{{todo.message}}
      </p>
      <p>
        <strong>Status: </strong>{{todo.status}}
      </p>
    </div>
  </body>
  </html>
```

[[**Back to top**](#todo-list-application-in-flask-(part-ii))]

<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part1">
    <strong><--Prev</strong>
  </a>
</p>
<p align="right">
  <a href="#">
    <strong>Next--></strong>
  </a>
</p>


## Contributors:
<a href="https://github.com/ASHIK11ab">
  <img style="border-radius: 50px" src="https://avatars2.githubusercontent.com/u/58099865?s=460&u=dc835e2281a9265edf2b48059f1c8151be89a1b1&v=4" width="70px" height = "70px"> 
</a> 

[Ashik Meeran Mohideen](https://github.com/ASHIK11ab)

&copy; copyrights 2020. All rights reserved.

Licensed under [MIT LICENSE](https://github.com/ASHIK11ab/Flask-Series/blob/main/LICENSE)
