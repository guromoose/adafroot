"""
Lager et bord som heter potlog i databasen tmp_db
"""

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine("mysql://root:toor@localhost/tmp_db", echo=True)
Base = declarative_base()

class Potlog(Base):
	""""""
	__tablename__ = "potlog"

	id = Column(Integer, primary_key=True)
	value = Column(String(10))
	time = Column(DateTime)

	def __init__(self, value, time):
		""""""
		self.value = value
		self.time = time

# create tables
Base.metadata.create_all(engine)