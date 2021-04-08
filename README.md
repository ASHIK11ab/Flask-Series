## Todo list application in Flask (Part I)

### Overview
- In this episode we are going to create the frontend required for our todo list application using Flask.
- To see the YouTube demonstration of this tutorial [click here](https://youtu.be/P1Gj-OK2oXg)

| &emsp;&emsp;&emsp;Table of Contents |
| --- |
| 1. [**Creating our application**](#creating-our-application) |
| 2. [**Creating a layout file**](#creating-a-layout-file) |
| 3. [**Creating index.html**](#creating-index.html) |
| 4. [**Styling our elements**](#styling-our-elements) |
| 5. [**Final touch with JavaScript**](#final-touch-with-javascript) |

### Setting up the environment
- Download this [Pipfile.lock](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part1/Pipfile.lock) and install the necessary dependencies by running
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
#### Creating our application
1. Lets first create our application.
```python
  from flask import Flask, render_template

  app = Flask(__name__)
```

2. Lets create an index route where we will be returning an index.html template.
```python
  @app.route('/')
  def home():
    return render_template('index.html')
```

#### Creating a layout file
3. Before creating the index.html file lets first create a layout.html file which we will be using as a layout so that other templates can inherit from this layout file.

4. In the layout.html file lets create a blocks for title, stylesheet, body, script.
```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="{{ url_for('static', filename='/css/index.css') }}">
  <title>
    {% block title %} {% endblock %}
  </title>
  <style>
    {% block stylesheet %} {% endblock %}
  </style>
  </head>
  <body>
    {% block body %} {% endblock %}

    {% block script %} {% endblock %}
  </body>
  </html>
```

> We have also linked a index.css file using jinja2 syntax. We will be doing all our styling in the index.css file.

5. Since our application is going to have a navigation bar, lets create it in our layout file.
```html
  <nav class="navbar">
    <div class="container">
      <h2>Todo App</h2>
      <ul>
        <li>
          <a href="{{ url_for('home') }}">Home</a>
        </li>
        <li>
          <a href="#">Complete</a>
        </li>
      </ul>
    </div>
  </nav>
```

6. Consolidating our [layout.html should look like this now](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part1/templates/layout.html).

7. Now lets first style the navbar in index.css.<br>
&emsp;i. Lets first set the font family of all elements to helvetica.
  ```css
      * {
        font-family: Helvetica;
      }
  ```
&emsp;&emsp;&emsp;&emsp;ii. Lets give background color and some padding to the navbar, lets use the container to give whitespace in both sides.
  ```css
      .navbar {
      background: #fff;
      border-bottom: 1px solid #000;
      padding: .5rem;
      }

      .container {
        width: 80%;
        margin: auto;
      }

      .navbar .container {
        display: flex;
      }
  ```

> We are displaying the container inside the navbar as flex since we want all of the elements in navbar to be displayed in a row.

&emsp;&emsp;&emsp;&emsp;iii. For the <kbd>ul</kbd> in the navbar lets display the list items in same row and lets remove some of the default styling to make our navbar look a little bit nice.
```css
    .navbar ul {
    display: flex;
    list-style: none;
    margin-left: 1rem;
    }

    .navbar ul li a {
      text-decoration: none;
      color: #000;
      margin-left: 1rem;
      font-size: 1rem;
    }
```

#### Creating index.html
8. Now lets create an index.html file which will inherit from the layout file.

9. In the block body lets create a form inside of a <kbd>div</kbd>.
```html
  {% extends "layout.html" %}

  {% block title %}
    Todo App in Flask
  {% endblock %}

  {% block body %}
    <button id="add-todo">Add todo</button>
    <div id="modal">
      <form action="{{ url_for('home') }}" class="closed" id="modal-form" method=post>
        <span id="close-btn">&times;</span>
        <h2>Add Todo details</h2>
        <label>Title:</label>
        <input type="text" maxlength=20 name="title">

        <label>Message:</label>
        <textarea name="message"></textarea>

        <button>Submit</button>
      </form>
    </div>
  {% endblock %}

  {% block script %}
    <script src="{{ url_for('static', filename='/js/index.js') }}"></script>
  {% endblock %}
```
> We will use the javascript file later on.

#### Styling our elements
10. Now lets style the add todo button. We will position it to right of the window with some background color and lets also add some padding.
```css
  button {
    margin-top: 1rem;
    position: absolute;
    right: 1rem;
    background: rgb(113, 68, 197);
    color: #fff;
    border: 0;
    width: 100px;
    border-radius: 15px;
    cursor: pointer;
    padding: .9rem;
  }
```

11. Now we need to style the form and elements inside it.<br>
&emsp;i. Lets give the form a fixed width and height and lets position the form in the center with some padding and border.
```css
    form {
      position: absolute;
      top: -800px;
      left: 50%;
      transform: translate(-50%);
      width: 500px;
      height: 400px;
      background: #fff;
      padding: 2rem;
      border-radius: 8px;
      transition: top .8s;
      border: 1.5px solid #ddd;
    }
```
> We initially set the form with a top value of -800px so that we can later on use javascript to display the form from top when the add todo button is clicked.

&emsp;&emsp;&emsp;&emsp;ii. Now lets display the label, input and textarea as block elements and lets also do some basic styling to these elements.
```css
    label {
      display: block;
      font-size: 1rem;
    }

    input, textarea {
      box-sizing: border-box;
      border: 2px solid #ddd;
      border-radius: 8px;
      outline: none;
      padding: .5rem;
      margin: 1rem 0;
      display: block;
      width: 100%;
    }

    textarea {
      resize: none;
      height: 100px;
    }
```
> The we set the resize property of textarea to none since we dont want it to resize.

&emsp;&emsp;&emsp;&emsp;iii. Now when the input and textarea is focused we need to highlight them by changing the border.
```css
    input:focus, textarea:focus {
      border: 2px solid dodgerblue;
      transition: .6s;
    }
```
&emsp;&emsp;&emsp;&emsp;iv. Now lets align the <kbd>h2</kbd> tag to center and lets position the <kbd>span</kbd> element to the top right of the form.
```css
    form h2 {
      text-align: center;
    }

    form span {
      position: relative;
      top: 1rem;
      left: 95%;
      font-size: 2rem;
      font-weight: bold;
      color: #ddd;
    }

    form span:hover {
      cursor: pointer;
      color: #000;
    }
```
&emsp;&emsp;&emsp;&emsp;v. Lets display the button in the form with a width of 90% and with some padding and some basic styling.
```css
    form button {
      width: 90%;
      background: dodgerblue;
      color: #fff;
      padding: .5rem;
      border: 0;
      border-radius: 8px;
      box-sizing: border-box;
    }
```
12. Now lets style a class <kbd>.bg-dark</kbd> which we will be adding as a background to the <kbd>form</kbd> element.
```css
  .bg-dark {
    position: fixed;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, .7);
    margin-left: -.5rem;
  }
```

13. Consolidating our [index.css should look like this.](https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part1/static/css/index.css)

#### Final touch with JavaScript
14. Now we need to display the form from the top only when the click on the add todo button. For this we will be using JavaScript.

15. Lets first declare the variables which are required.
```js
  let add_icon = document.getElementById("add-todo");
  let modal = document.getElementById("modal");
  let form = document.getElementById("modal-form");
  let close_btn = document.getElementById("close-btn");
```
16. First lets create two functions <kbd>show_form()</kbd> and <kbd>hide_form()</kbd> which will show and hide the form.
```js
  function show_form() {
    if(form.className == "closed") {
      form.style.top = "15%";
      form.className = "opened";
      modal.classList.add('bg-dark');
    }
  }

  function hide_form() {
    form.style.top = "-800%";
    form.className = "closed";
    modal.classList.remove('bg-dark');
  }
```
> We are adding a the bg-dark class to the modal so that when form is diplayed we get a dark color in the background and we remove it when the form is closed.
17. Now we need to call the <kbd>show_form()</kbd> function when the add todo button is clicked so we create a event listner for the add todo button.
```js
  add_icon.addEventListener('click', show_form);
```
18. Next, when the user clicks the close button in the form we need to call the <kbd>hide_form()</kbd> function. So, we create another event listener.
```js
  close_btn.addEventListener('click', hide_form);

```
19. Now, when the form is opened and when user clicks outside the form we need to hide the form.
```js
  window.addEventListener('click', function(event){
    if(form.className == "opened" && event.target == modal)
      hide_form();
  });
```

[[**Back to top**](#todo-list-application-in-flask-(part-i))]

<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/orm">
    <strong><--Prev</strong>
  </a>
</p>
<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2">
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
