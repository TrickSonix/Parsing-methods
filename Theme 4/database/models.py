from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Apartments(Base):
    __tablename__ = 'apartments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    name = Column(String)
    cost = Column(Integer)
    autor_id = Column(Integer, ForeignKey('autors.id'))
    autor = relationship('Autors', backref='apartments')

    def __init__(self, url, name, cost, autor_id):
        self.url = url
        self.name = name
        self.cost = cost
        self.autor_id = autor_id

class ImagesUrls(Base):
    __tablename__ = 'imagesurls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    apartment_id = Column(Integer, ForeignKey('apartments.id'))
    url = Column(String, unique=True)
    images = relationship('Apartments', backref='apartments')
    def __init__(self, apartment_id, url):
        self.apartment_id = apartment_id
        self.url = url

class Autors(Base):
    __tablename__ = 'autors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    name = Column(String)

    def __init__(self, url, name):
        self.url = url
        self.name = name