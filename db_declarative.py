import os, sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    baselineMood = Column(Float)
    sessionMood = Column(Float)

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment = Column(String(250))
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

# Create engine to store data in local db
engine = create_engine('sqlite:///comments.db')

#Create tables in engine
Base.metadata.create_all(engine)
