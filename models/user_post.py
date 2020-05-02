from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from models.engine import Base
from models.channel import Channel

upvote_association_table = Table('upvotes', Base.metadata,
                            Column('post_id', Integer, ForeignKey('post.id')),
                            Column('user_id', Integer, ForeignKey('user.id')))

downvote_association_table = Table('downvotes', Base.metadata,
                            Column('post_id', Integer, ForeignKey('post.id')),
                            Column('user_id', Integer, ForeignKey('user.id')))

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    post_id = Column(Integer)
    post_text = Column(String(4096))
    channel = relationship('Channel', back_populates='posts')
    upvote_users = relationship('User', secondary=upvote_association_table, back_populates='upvote_posts')
    downvote_users = relationship('User', secondary=downvote_association_table, back_populates='downvote_posts')

    def upvotes(self):
        return len(self.upvote_users)

    def downvotes(self):
        return len(self.downvote_users)

    def __repr__(self):
        return self.post_text

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship('Channel', back_populates='users')
    upvote_posts = relationship('Post', secondary=upvote_association_table, back_populates='upvote_users')
    downvote_posts = relationship('Post', secondary=downvote_association_table, back_populates='downvote_users')