from models.engine import Base, db_engine, db_session
from models.channel import Channel

def add_record(record):
    db_session.add(record)
    db_session.commit()

def create_tables():
    Base.metadata.create_all(db_engine)

def add_channel(ch_id: int):
    new_channel = Channel(channel_id=ch_id, current=True)
    if db_session.query(Channel).filter(Channel.channel_id==new_channel.channel_id).first() is None:
        add_record(new_channel)
        return True
    else:
        return False

def get_current_channel():
    current_channel = db_session.query(Channel).filter(Channel.current==True).first()
    if current_channel is None:
        return False
    else:
        return current_channel
    