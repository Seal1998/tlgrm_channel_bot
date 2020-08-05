from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from models.engine import Base, db_session

class DelayedPost(Base):
    __tablename__ = 'delayed_post'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship('Channel', back_populates='delayed_posts')

    text = Column(String)
    has_media = Column(Boolean, default=False)
    media_photo = Column(Boolean, default=False)
    media_path = Column(String)

    def save_media(self, media):
        self.has_media = True
        if type(media).__name__ == 'PhotoSize':
            self.media_photo = True
            photo = media.get_file().download(custom_path='PROJECT DIR/delayed_posts/...')