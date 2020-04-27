from sqlalchemy import Column, Integer, Boolean
from models.engine import Base

class User(Base):
    __tablename__ = 'user'