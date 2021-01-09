from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://<your username>:<your password>@localhost:5432/<database name>')
db = scoped_session(sessionmaker(bind = engine))


# Returns all the rows from the student table.
def show_students():
  students = db.execute("select * from student").fetchall()
  for student in students:
    print(student)


# Adds a student to the student table.
def add_student(name, age):
  db.execute(f"insert into student (name, age) values ('{name}', {age})")
  db.commit()
  print("Added student")
  show_students()


# Deletes a student from the table.
def delete_student(id):
  db.execute(f"delete from student where id = {id}")
  db.commit()
  print("Deleted student")
  show_students()