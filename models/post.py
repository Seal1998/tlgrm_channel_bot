from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from models.engine import Base

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
    channel = relationship('Channel', back_populates='posts')
    upvote_users = relationship('User', secondary=upvote_association_table, back_populates='upvote_posts')
    downvote_users = relationship('User', secondary=downvote_association_table, back_populates='downvote_posts')

    def upvotes(self):
        return len(self.upvote_users)

    def downvotes(self):
        return len(self.downvote_users)

    def __repr__(self):
        return self.post_text