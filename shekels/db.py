from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

from flask_login import UserMixin

Base = declarative_base()


class DB:
    def __init__(self, db_name, debug=False):
        connection_string = 'sqlite:///' + db_name
        self.engine = create_engine(connection_string, echo=debug)
        self.session_maker = scoped_session(sessionmaker(bind=self.engine))
        self.session = None

    def get_session(self):
        if not self.session:
            self.session = self.session_maker()

        return self.session

    def close_session(self):
        if self.session:
            self.session.close()

    def create_db(self):
        Base.metadata.create_all(self.engine)


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    full_name = Column(String)
    password = Column(String)

    def __str__(self):
        return "User: {} {}".format(self.login,
                                    self.full_name)


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)