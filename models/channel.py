from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from models.engine import Base
from models.user_admin import allowed_channels_association_table

class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    channel_title = Column(String(length=100))
    channel_username = Column(String(length=100))
    posts = relationship('Post', back_populates='channel')
    delayed_posts = relationship('DelayedPost', back_populates='channel')
    users = relationship('User', back_populates='channel')
    in_user_context = relationship('AdminUser', back_populates='current_channel')
    admin_users = relationship('AdminUser', secondary=allowed_channels_association_table, back_populates='allowed_channels')

    def __repr__(self):
        return str(self.channel_id)