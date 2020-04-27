from sqlalchemy import Column, Integer, Boolean
from models.engine import Base

class Post(Base):
    __tablename__ = 'posts'