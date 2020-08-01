from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from models.engine import Base, db_session
from models.post import upvote_association_table, downvote_association_table

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    channel_id = Column(Integer, ForeignKey('channel.channel_id'))
    channel = relationship('Channel', back_populates='users')
    upvote_posts = relationship('Post', secondary=upvote_association_table, back_populates='upvote_users')
    downvote_posts = relationship('Post', secondary=downvote_association_table, back_populates='downvote_users')