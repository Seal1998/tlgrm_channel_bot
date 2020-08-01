
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.engine import Base, db_session

class AdminUser(Base):
    __tablename__ = 'admin_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    current_channel_id = Column(Integer, ForeignKey('channel.channel_id'))
    current_channel = relationship('Channel', back_populates='in_user_context')

    def change_channel_context(self, new_current_channel_id):
        self.current_channel_id = new_current_channel_id
        db_session.commit()