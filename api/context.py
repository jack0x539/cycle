from api.models import User, Address, EventRole, Base
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

class Context:
    hostname = None
    database = None
    username = None
    password = None

    last_error = None
    erred = False

    engine = None
    Session = sessionmaker()

    def __init__(self, hostname, database, username, password):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password

        self.engine = sqlalchemy.create_engine("sqlite:///cycle.sqlite")
        Base.metadata.create_all(self.engine)
        self.Session.configure(bind=self.engine)

    def set_error(self, error):
        self.last_error = error
        self.erred = True

    def clear_error(self):
        self.last_error = None
        self.erred = False

    def get_users(self):
        self.clear_error()

        session = self.Session()
        users = session.query(User).all()
        return users
    
    def get_user(self, id):
        self.clear_error()

        session = self.Session()
        user = session.query(User).filter(User.id == id).first()
        return user

    def create_user(self, username, forename, surname, email, dob_str):
        self.clear_error()

        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        user = User(username=username, forename=forename, surname=surname, email_address=email, dob=dob)
        session = self.Session()
        session.add(user)
        session.commit()

        return user




