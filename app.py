from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = "This should be really secret"

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/<string:user>')
def say_hello(user):
  return render_template("variables.html", user = user, cnt = len(user))

languages = ["python", "HTML", "CSS", "JS"]

@app.route('/for_loops')
def for_loops():
  return render_template("for_loops.html", languages = languages)

@app.route('/ifElse')
def ifElse():
  return render_template("ifElse.html", languages = languages)

@app.route('/for_inherited')
def for_inherited():
  return render_template("for_loops_inherited.html", languages = languages)


@app.route('/ifElse_inherited')
def ifElse_inherited():
  return render_template("ifElse_inherited.html", languages = languages)

@app.route('/form', methods=["GET", "POST"])
def form():
  if request.method == "POST" :
    name = request.form['name']
    age = request.form.get('age')
    return render_template("response.html", name = name, age = age)

  return render_template("form.html")

db = {
  "user1": "pass1",
  "user2": "pass2",
  "user3": "pass3"
}

@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST" :
    username = request.form.get('username')
    password = request.form.get('password')

    if username not in db.keys():
      return "<h1 style='color: red'> You have no account </h1>"

    if db[username] != password:
      return "<h1 style='color: red'> You Password was incorrect </h1>"

    session['user'] = username
    return redirect(url_for('Dashboard'))
    

  return render_template("login.html")

@app.route('/Dashboard')
def Dashboard():
  return render_template("login_response.html")

if __name__ == "__main__":
  app.run(debug=True)