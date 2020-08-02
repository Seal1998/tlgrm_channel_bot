
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.engine import Base, db_session

allowed_channels_association_table = Table('allowed_user_channel', Base.metadata,
                                        Column('channel_id', Integer, ForeignKey('channel.id')),
                                        Column('adminuser_id', Integer, ForeignKey('admin_user.id')))

class AdminUser(Base):
    __tablename__ = 'admin_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    user_type = Column(String)
    current_channel_id = Column(Integer, ForeignKey('channel.channel_id'))
    current_channel = relationship('Channel', back_populates='in_user_context')
    allowed_channels = relationship('Channel', secondary=allowed_channels_association_table, back_populates='admin_users')

    def change_channel_context(self, new_current_channel_id):
        self.current_channel_id = new_current_channel_id
        db_session.commit()

    def channel_allowed(self, channel_id_to_check):
        channel_ids = [channel.channel_id for channel in self.allowed_channels]
        if channel_id_to_check in channel_ids:
            return True
        else:
            return False

    def add_allowed_channel(self, new_channel):
        self.allowed_channels.append(new_channel)
        db_session.commit()