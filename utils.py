import validators
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = 'postgresql://ashik:ashikmeeran11@localhost:5432/url_shortner'
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind = engine))

def valid_url(url):
  return validators.url(url) is True

def name_available(name):
  return db.execute("select short_name from url_info where short_name = :name",
  {"name" : name}).fetchone()

def add_url(name, url):
  db.execute("insert into url_info (short_name, url) values (:name, :url)",
  {
    "name": name,
    "url": url
  })
  db.commit()

def get_url(short_name):
  return db.execute("select * from url_info where short_name = :short_name",
  {"short_name" : short_name}).fetchone()

