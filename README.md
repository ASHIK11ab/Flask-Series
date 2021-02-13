## Object Relation Mapping (ORM) in Flask

### Overview
- In this episode we will explore on how to use Object Relational Mapping (ORM) in Flask using Flask-SQLAlchemy.
- ORM is a powerful tool which lets us combine object oriented programming along with SQL.
- The basic idea behind ORM is that we model an SQL table as a class and then we use certain methods to query the database.
- To see the YouTube demonstration of this tutorial [click here]()

### Setting up the environment
- Download this [Pipfile.lock](https://github.com/ASHIK11ab/Flask-Series/tree/orm/Pipfile.lock) and install the necessary dependencies by running
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

### Step by Step Guide
1. Import necessary classes.
```python
  from flask import Flask
  from flask_sqlalchemy import SQLAlchemy
```

2. Now lets create our Flask application.
```python
  app = Flask(__name__)
```
> We are not going to be creating a web app. But Flask-SQLAlchemy uses our application's configuration values for the database URI.

3. Lets set a couple of configuration values for our app.
```python
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<your username>:<your password>@localhost:5432/<database_name>'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

4. Now we need to create our database object.
```python
  db = SQLAlchemy(app)
```

### Modelling a table as a Class
1. Now its time to model an SQL table as a class.
```python
  class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
```
  &emsp;&emsp;&emsp;i. We have created a class called User which inherits from the class db.Model.<br>
  &emsp;&emsp;&emsp;ii. The '\_\_tablename__' is used to specify the name of table.<br>
  &emsp;&emsp;&emsp;iii. We have created 3 columns in our table namely id, name, age.<br>
  &emsp;&emsp;&emsp;iv. The method db.Column() creates an column.
  > - primary_key = True tells Flask-SQLAlchemy that this column is going to be our primary key.
  > - nullable = False tells Flask-SQLAlchemy to not allow NULL values in this column.

2. Lets also give a printable representation of our object so that we can see the output in a formatted way.
```python
  def __repr__(self):
    return f'({self.id}, {self.name}, {self.age})'
```

### Note
- From now on all the commands which we execute will be from the python interpreter.
- Before going forward dont forget to import [models.py](https://github.com/ASHIK11ab/Flask-Series/tree/orm/models.py)
```python
  from models import *
```

### Converting classes to tables
1. Now we need to convert our classes into SQL tables.
```python
  > db.create_all()
```
  > db.create_all() will convert all our classes into SQL tables automatically.

2. Now our database should look like this.
```postgres
  orm=> \d
            List of relations
  Schema |     Name     |   Type   | Owner
  --------+--------------+----------+-------
  public | users        | table    | ashik
  public | users_id_seq | sequence | ashik
  (2 rows)
```

### Inserting records into the table 
1. Inorder to insert records into the table. First we need to create an object of our class.
```python
  user = User(name = 'Jack', age = 21)
```
2. Now we need to add this object to our table.
```python
  db.session.add(user)
  db.session.commit()
```
&emsp;&emsp;&emsp;i. Since we are making a changes to the table we need to run db.session.commit() to commit all our changes.

3. You can add more than one object to the table by using db.session.add_all() method.
```python
  user1 = User(name = 'James', age = 19)
  user2 = User(name = 'Harry', age = 18)
  user3 = User(name = 'Kim', age = 16)
  db.session.add_all([user1, user2, user3])
  db.session.commit()
```

### Selecting records from a table
1. To select all the values from the table users.
```sql
  SQL query:

  select * from users;
```
```python
  Equivalent ORM query:

  users = User.query.all()
  print(users)
```
- The result of above ORM query is:
```postgres
   id | name  | age
  ----+-------+-----
    1 | Jack  |  21
    2 | James |  19
    3 | Harry |  18
    4 | Kim   |  16
  (3 rows)
```