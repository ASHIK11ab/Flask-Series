from flask import Flask, request, render_template, redirect
from utils import *

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    short_name = request.form.get('name')
    url = request.form.get('url')

    if 'http' not in url:
      url = f'http://{url}'
    
    if valid_url(url):
      if name_available(short_name) is None:
        add_url(short_name, url)
        return render_template("success.html", short_name=short_name)
      else:
        return render_template('index.html', msg='Short name not available')
    else:
      return render_template('index.html', msg='Invalid url')

  return render_template('index.html')


@app.route('/<path:short_name>')
def redirect_url(short_name):
  url = get_url(short_name)
  if url is None:
    return "<h2 style='color:red'> Invalid URL </h2>"
  return redirect(url.url)