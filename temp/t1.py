# Tworzymy silnik bazy danych
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
engine = create_engine('sqlite:///test.db', echo=True)

# tworzymy podstawy do deklaratywnego definiowania
# bazy danych
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __str__(self):
        return "User: {} {}".format(self.name, self.fullname)

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", backref="addresses")

# Tylko za pierwszym razem
Base.metadata.create_all(engine)



Session = sessionmaker(bind=engine)
session = Session()






