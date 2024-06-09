from sqlalchemy import Column, CHAR, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
import datetime

# Defining the base class
Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


# Defining the Restaurants class to represent the Restaurants table
class Restaurants(Base):
    __tablename__ = 'restaurants'

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
# Defining the Menu class to represent the menus table
class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(CHAR(36), nullable=False)
    item_name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    




