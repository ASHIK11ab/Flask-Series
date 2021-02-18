## Connecting to Database from Python

### Overview
- In this tutorial we will learn how to connect to a database from Python and we will also execute some basic SQL queries from Python.
- To see the YouTube demonstration of this tutorial [click here](https://youtu.be/UBf1z4sVV10)

### Setting up the environment
- Install the necessary dependencies by running
  ```bash
    > pipenv sync
  ```
- This will install the dependencies from Pipfile.lock

### Note:
> - Since pipfile varies accross various operating systems. If you get into trouble installing the dependencies. Then,
> - Manually install the dependencies by running
>  ```bash
>   > pipenv install SQLAlchemy psycopg2
>  ```

### Step by Step Guide
1. First in order to connect to a database we need to do a bunch of imports.
```python
  from sqlalchemy import create_engine
  from sqlalchemy.orm import scoped_session, sessionmaker

```

2. Then we need to create a database engine which will be responsible for execute our SQL queries from Python and it will get back the results.
```python
  engine = create_engine('postgresql://<your username>:<your password>@localhost:5432/<database name>')
```

3. We create a seprate session for each user so that one users usage of the database object does not interfere with other users.
```python
  db = scoped_session(sessionmaker(bind = engine))
```

4. Now we will create a bunch of functions to demonstrate how we can execute SQL queries from Python.
```python
  # Returns all the rows from the student table.
  def show_students():
    students = db.execute("select * from student").fetchall()
    for student in students:
      print(student)
```
```python
  # Adds a student to the student table.
  def add_student(name, age):
    db.execute(f"insert into student (name, age) values ('{name}', {age})")
    db.commit()
    print("Added student")
    show_students()
```
```python
  # Deletes a student from the table.
  def delete_student(id):
    db.execute(f"delete from student where id = {id}")
    db.commit()
    print("Deleted student")
    show_students()
```

[[Back to top](#connecting-to-database-from-python)]

<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/flask-crash-course">
    <strong><--Prev</strong>
  </a>
</p>
<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/url-shortner-app">
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
