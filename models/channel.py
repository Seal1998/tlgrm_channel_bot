from sqlalchemy import Column, Integer, Boolean
from models.engine import Base

class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    current = Column(Boolean, default=True)

    def __repr__(self):
        return str(self.channel_id)