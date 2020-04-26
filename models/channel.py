from sqlalchemy import Column, Integer
from models.engine import Base, db_engine

class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)

    def __repr__(self):
        return self.id

if __name__ == '__main__':
    Base.metadata.create_all(engine)