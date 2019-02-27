import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Text, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def connect(db):
    engine = create_engine(_database_path(db))
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def _database_path(db):
    return 'sqlite:///' + os.path.abspath(db)

class Spiral(Base):
    __tablename__ = 'spiral'
    id = Column(Integer, primary_key=True)
    nodes = Column(Text, nullable=False)
    frequency_results = Column(Text, nullable=False)
    phase_results = Column(Text, nullable=False)
    # These two columns are JSON objects, but sqlite has no JSON data type. 
    # As such, these must be stored as text, but all abstractions will immediately 
    # convert to JSON (or dict) before interacting with them
    # TODO: sqlalchemy 1.3 will support JSON for sqlite
    rf_data = Column(Text, nullable=False)
    vision_data = Column(Text, nullable=False)
