from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from models.engine import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    post_id = Column(Integer)
    post_text = Column(String(4096))
    channel = relationship('Channel', back_populates='posts')

    def __repr__(self):
        return self.post_text