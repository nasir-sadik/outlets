import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    name = Column(String(250))

    @property
    def serialize(self):
            return {
            'email': self.email,
            'name': self.name,
            'id': self.id,
        }


class Outlet(Base):
    __tablename__ = 'outlet'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    outlet_id = Column(Integer, ForeignKey('outlet.id'))
    outlet = relationship(Outlet, backref='items')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'outlet_id': self.outlet_id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }


engine = create_engine('sqlite:///outletDB.db')


Base.metadata.create_all(engine)
