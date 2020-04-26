from models.engine import Base, db_engine
from models.channel import Channel

class Db():
    @staticmethod
    def create_tables():
        Base.metadata.create_all(db_engine)

    @staticmethod
    def set_channel(channel_id: int)
        
    