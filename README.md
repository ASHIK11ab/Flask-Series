## Files in Flask

### Overview
- In this episode we will be seeing on how to upload files using Flask and how to send attachments using Flask.
- To see the YouTube demonstration of this episode [click here.](https://youtu.be/Bj4cjo5R_6s)

| &emsp;&emsp;&emsp;Table of Contents |
| --------------------------- |
| 1. [**Creating the application**](#creating-our-application) |
| 2. [**Uploading single file**](#uploading-single-file) |
| 3. [**Uploading multiple files**](#uploading-multiple-files) |
| 4. [**Sending files as attachment**](#sending-files-as-attachment) |


### Setting up the environment
- Download this [Pipfile.lock](https://github.com/ASHIK11ab/Flask-Series/tree/files-in-flask/Pipfile.lock) and install the necessary dependencies by running
```bash
  > pipenv sync
```
- This will install the dependencies from Pipfile.lock

### Note:
> - Since pipfile varies accross various operating systems. If you get into trouble installing the dependencies. Then,
> - Manually install the dependencies by running
>  ```bash
>   > pipenv install Flask
>  ```

### Step by Step Guide

### Creating our application

1. First lets do a whole bunch of imports which are required. We will be using some imported functions later on in this episode.
```python
  import os
  from flask import Flask, render_template, redirect, flash, request, send_from_directory
  from werkzeug.utils import secure_filename
```

2. Now lets create our application and since we will be using <kbd>flash</kbd>, lets also set a <kbd>secret key</kbd> for our application.
```python
  app = Flask(__name__)

  app.config['SECRET_KEY'] = '<your secret key goes here>'
```

### Uploading single file

3. Lets create a <kbd>/</kbd> route where we will return a <kbd>index.html</kbd> template.
```python
  @app.route('/')
  def index():
    return render_template('index.html')
```

4. In the <kbd>index.html</kbd> lets create a <kbd>form</kbd> by which users can upload a file.
```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Files in Flask</title>
  </head>
  <body>
    <div class="container">
      <h1>Upload your files here</h1>
      <p>Upload only png, jpg, jpeg, gif images only.</p>
      <form action="/" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Upload">
      </form>
    </div>
  </body>
  </html>
```
> - In order to allow the users to upload a file we should set the <kbd>enctype</kbd> attribute of the input filed to <kbd>"multipart/form-data"</kbd>.

5. Now lets do some basic styling for the index page using a <kbd>style</kbd> tag.
```html
  <style>
    .container {
      width: 80%;
      margin: 2rem auto;
    }

    input {
      display: block;
      margin-bottom: 2rem;
      font-size: 18px;
    }

    input[type="submit"] {
      background-color: dodgerblue;
      color: #fff;
      padding: .8rem;
      border-radius: 10px;
    }

    .error {
      color: #ff0000;
    }
  </style>
```

6. Now we need to jump to our backend inorder to save the uploaded image.

7. Before proceeding further, lets create a <kbd>images</kbd> directory inside of a <kbd>uploads</kbd> directory where all our uploaded images will be saved.

8. Our directory structure should look like this.
```
  /
  |___ templates/
  |___ uploads/
       |___ images/
```

9. Now lets create a <kbd>utils.py</kbd> file where we will be creating some utilitie functions, because i like to keep my application file <kbd>app.py</kbd> clean.

10. In <kbd>utils.py</kbd><br>
&nbsp;&nbsp;&nbsp;&nbsp;i. Lets create a variable called <kbd>ALLOWED_EXTENSIONS</kbd> which will be a list of extensions of files the user can upload.<br>
&nbsp;&nbsp;&nbsp;&nbsp;ii. Lets also create a variable called <kbd>UPLOADS_FOLDER</kbd> which will be the path to where the uploaded images should be saved.
```python
  ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

  UPLOADS_FOLDER = 'uploads/images/'
```

11. Now lets import everything from <kbd>utils.py</kbd> to our <kbd>app.py</kbd>
```python
  from utils import *
```

12. Now set the <kbd>UPLOADS_FOLDER</kbd> as a configuration variable (not mandatory for convienience only).

13. Now since the <kbd>/</kbd> route is going to be accepting a <kbd>POST</kbd> request, we need to specify the list of methods that the <kbd>/</kbd> route will accept.
```python
  @app.route('/', methods=["GET", "POST"])
  def index():
    if request.method == "GET":
      return render_template('index.html')
```
> - If the request method was a <kbd>GET</kbd> method we simply return the <kbd>index.html</kbd>.

14. Now we need to get the uploaded file in the backend. We can get the incoming file by using <kbd>request.files['\<name given in input field>']</kbd>.

15. There are a bunch which will need to validate before saving the file.<br>
&nbsp;&nbsp;&nbsp;&nbsp;i. First we need to make sure that the <kbd>POST</kbd> request has a file part in it. If not, flash a message.
```python
  if not 'file' in request.files:
    flash('No file part in request')
    return redirect(request.url)
```
&emsp;&emsp;&emsp;&nbsp;ii. Now we need to get the file by using the <kbd>request.files</kbd>.
```python
  file = request.files.get('name')
```
&emsp;&emsp;&emsp;&nbsp;iii. Next, we need to make sure that the user did not do a empty upload. If so, flash a message.
```python
  if file.filename == '':
    flash('No file uploaded')
    return redirect(request.url)
```
&emsp;&emsp;&emsp;&nbsp;iv. Before saving the file we need the make sure that the file extension is in the list of valid extensions. Lets do this by creating a <kbd>file_valid(file)</kbd> function in <kbd>utils.py</kbd>.
```python
  def file_valid(file):
    return '.' in file and \
      file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
```
&emsp;&emsp;&emsp;&nbsp;v. Now if the filename is valid we can save the file using the <kbd>save()</kbd> method in the file object. If not, flash a error.
```python
  if file_valid(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
  else:
    flash('File type not supported')
    return redirect(request.url)
```
> - The else block was not added in the YouTube video.
> - The <kbd>secure_filename()</kbd> returns a secure name of the file which can be added to the file system in case if the filename contained was something like '../../../.bashrc'.

16. Consolidating our <kbd>/</kbd> route should look like this now.
```python
  @app.route('/', methods=["GET", "POST"])
  def index():
    if request.method == "GET":
      return render_template('index.html')

    if not 'file' in request.files:
      flash('No file part in request')
      return redirect(request.url)

    file = request.files.get('file')

    if file.filename == '':
      flash('No file uploaded')
      return redirect(request.url)

    if file_valid(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
    else:
      flash('File type not supported')
      return redirect(request.url)
    
    return "File uploaded successfully"
```

17. While processing the files we flashed a lot of messages. Now lets gets the flashed messages in the index page using <kbd>Jinja</kbd>.
```jinja
  {% with messages = get_flashed_messages() %}
    {% for msg in messages %}
      <p class="error">{{ msg }}</p>
    {% endfor %}
  {% endwith %}
```
> Add this <kbd>with</kbd> block inside the <kbd>container</kbd> <kbd>div</kbd>.

18. We have successfully completed on uploading and processing a single uploaded file.

### Uploading multiple files

19. Now, lets see on how to upload and process multiple files in Flask.

20. First inorder to allow the user to upload multiple files add the <kbd>multiple</kbd> attribute to the <kbd>input</kbd> filed in index.html.
```html
  <input type="file" name="file" multiple required>
```

21. Now, we just need to refactor a little bit in the backend inorder to process and save multiple files.<br>
&nbsp;&nbsp;i. First inorder to get all of the uploaded files we use the <kbd>request.files.getlist()</kbd> method.
```python
  files = request.files.getlist('file')
```
&emsp;&emsp;&emsp;&nbsp;ii. Now we need to iterate through each file and if the files are valid we save them.
```python
  for file in files:
    if file.filename == '':
      flash('No file uploaded')
      return redirect(request.url)

    if file_valid(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
    else:
      flash('File type not supported')
      return redirect(request.url)

  return "Files uploaded successfully"
```

22. Consolidating for uploading multiple files our <kbd>/</kbd> route should look like this now.
```python
  @app.route('/', methods=["GET", "POST"])
  def index():
    if request.method == "GET":
      return render_template('index.html')
    
    if not 'file' in request.files:
      flash('No file part in request')
      return redirect(request.url)

    files = request.files.getlist('file')

    for file in files:
      if file.filename == '':
        flash('No file uploaded')
        return redirect(request.url)

      if file_valid(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
      else:
        flash('File type not supported')
        return redirect(request.url)
        
    return "Files uploaded successfully"
```

### Sending files as attachment

23. Now, lets see on how to send files as attachments. Inorder to send files as attachment we will be using <kbd>send_from_directory()</kbd> function in Flask.

24. Whenever the user goes into <kbd>/uploads/images/\<filename></kbd> we want to send the file as a attachment.
```python
  @app.route('/uploads/images/<path:filename>')
  def send_attachment(filename):
    return send_from_directory(app.config['UPLOADS_FOLDER'], 
      filename = filename, as_attachment = True)
```
> - The <kbd>path</kbd> is a URL converter in Flask. Which is used to get the entire path in the URL which comes after /uploads/images/

25. Thats all it takes to send attachments in Flask. We just need the filename and the directory from where we are going to send the file.

- We have come to the end of this episode. Hope you learnt something new. If you have any queries just raise an issue.
- To see the YouTube demonstration of this episode [click here](https://youtu.be/Bj4cjo5R_6s).

[[**Back to top**](#files-in-flask)]

<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/todo-list-app-part2">
    <strong><--Prev</strong>
  </a>
</p>
<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/OAuth-implementation">
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