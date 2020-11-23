"""
Lager et bord som heter potlog i databasen tmp_db
"""

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

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