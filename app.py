from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/slink/<path:path_name>')
def index(path_name):
  return redirect(url_for(path_name, _external=True))