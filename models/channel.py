from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.orm import relationship
from models.engine import Base
from models.post import Post

class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    current = Column(Boolean, default=True)
    posts = relationship('Post', back_populates='channel')

    def __repr__(self):
        return str(self.channel_id)