## Object Relational Mapping in Flask

### Overview
- In this episode we will explore on how to use Object Relational Mapping (ORM) in Flask using Flask-SQLAlchemy.
- ORM is a powerful tool which lets us combine object oriented programming along with SQL.
- The basic idea behind ORM is that we model an SQL table as a class and then we use certain methods to query the database.
- To see the YouTube demonstration of this tutorial [click here](https://youtu.be/7C_zr5f9ed4)

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
<br>

| &emsp;&emsp;&emsp;&nbsp;Table of Contents |
| :---------------- |
| [**Modelling a SQL table as a class**](#modelling-a-sql-table-as-a-class) |
| [**Converting classes to tables**](#converting-classes-to-tables) |
| [**Inserting records into a table**](#inserting-records-into-a-table) |
| [**Selecting records from a table**](#selecting-records-from-a-table) |
| [**Filtering records based on condition**](#filtering-records-based-on-condition) |
| [**Updating records in a table**](#updating-records-in-a-table) |
| [**Deleting records in a table**](#deleting-records-in-a-table) |

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

### Modelling a SQL table as a Class
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
  >>> db.create_all()
```
  >>> db.create_all() will convert all our classes into SQL tables automatically.

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

### Inserting records into a table 
1. Inorder to insert records into the table. First we need to create an object of our class.
```python
  >>> user = User(name = 'Jack', age = 21)
```
2. Now we need to add this object to our table.
```python
  >>> db.session.add(user)
  >>> db.session.commit()
```
&emsp;&emsp;&emsp;i. Since we are making a changes to the table we need to run db.session.commit() to commit all our changes.

3. You can add more than one object to the table by using db.session.add_all() method.
```python
  >>> user1 = User(name = 'James', age = 19)
  >>> user2 = User(name = 'Harry', age = 18)
  >>> user3 = User(name = 'Kim', age = 16)
  >>> db.session.add_all([user1, user2, user3])
  >>> db.session.commit()
```

### Selecting records from a table
1. To select all the values from the table users.
```sql
  SQL query:

  select * from users;
```
```python
  Equivalent ORM Query:

  >>> users = User.query.all()
  >>> print(users)
```
```python
  Output:
    [(1, Jack, 21), (2, James, 19), (3, Harry, 18), (4, Kim, 16)]
```

2. For instance, if you only wanted the first record of the result you can use the first() method.
```python
  >>> user = User.query.first()
  >>> print(user)
```
```python
  Output:
    (1, Jack, 21)
```

3. If you only wanted to query specific columns then you can use the with_entities() method. For eg, If you only wanted the names of all of the users.

```sql
  SQL Query:

  select name from users;
```

```python
  Equivalent ORM Query:

  >>> user_names = User.query.with_entities(User.name).all()
  >>> print(user_names)
```
```python
  Output:
    [('Jack',), ('James',), ('Kim',)]
```

### Filtering records based on condition
1. We can filter the records based on certain conditions. For instance if you wanted to find the users whose age is greater than 18.
```sql
  SQL Query:

  select * from users where age > 18;
```
```python
  Equivalent ORM Query:

  >>> users = User.query.filter(User.age > 18).all()
```
```python
  Output:
    [(1, Jack, 21), (2, James, 19)]
```

2. You can also use multiple conditions to filter the results.<br>
&emsp;i. For instance lets get the details of all users whose age is greater than 20 or whose name starts with the character 'K'.
```sql
  SQL Query:

  select * from users where age > 20 or name like('K%');
```
```python
  Equivalent ORM Query:

  >>> users = User.query.filter( (User.age > 20) | (User.name.startswith('K')) ).all()
```
```python
  Output:
    [(1, Jack, 21), (4, Kim, 16)]
```

&emsp;&emsp;&emsp;&emsp;ii. Similar to 'or' condition ( ' | ' ) you can also use 'and' condition (' & ' ).<br>
&emsp;&emsp;&emsp;&emsp;iii. For instance lets get the details of all users whose id is greater than 2 and whose age is greater than 17.
```sql
  SQL Query:

  select * from users where id > 2 and age > 17;
```
```python
  Equivalent ORM Query:

  >>> users = User.query.filter( (User.id > 2) & (User.age > 17) ).all()
```
```python
  Output:
    [(3, Harry, 18)]
```

### Updating records in a table
1. Inorder to update any record or any field in a table we need to query the entire record and we need to update the value and we need to do a commit.

2. Lets try to update the age of all users by 1.
```python
  Before Updation:
  
    [(1, Jack, 21), (2, James, 19), (3, Harry, 18), (4, Kim, 16)]
```
```sql
  SQL Query:

  update users set age = age + 1;
```
```python
  Equivalent ORM Query:

  >>> users = User.query.all()
  >>> for user in users:
  ...  user.age += 1
  >>> db.session.commit()
```
```python
  Output (After Updation):
    [(1, Jack, 22), (2, James, 20), (3, Harry, 19), (4, Kim, 17)]
```

### Deleting records in a table
1. Now lets try to delete a record in a table. Lets try to delete the user with id 2.
```sql
  SQL Query:

  delete from users where id = 2;
```
```python
  >>> user = User.query.filter(User.id == 2).first()
  >>> db.session.delete(user)
  >>> db.session.commit()
```
```python
  Output (After Deleting):
    [(1, Jack, 22), (3, Harry, 19), (4, Kim, 17)]
```

[Back to top](#object-relational-mapping-in-flask)


<p align="right">
  <a href="https://github.com/ASHIK11ab/Flask-Series/tree/url-shortner-app">
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
