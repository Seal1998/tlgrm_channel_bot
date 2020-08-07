from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from models.engine import Base, db_session
from pathlib import Path
import uuid

class DelayedPost(Base):
    __tablename__ = 'delayed_post'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship('Channel', back_populates='delayed_posts')

    text = Column(String)
    has_media = Column(Boolean, default=False)
    media_photo = Column(Boolean, default=False)
    media_video = Column(Boolean, default=False)
    media_path = Column(String)

    def save_media(self, media):
        self.has_media = True
        if type(media).__name__ == 'PhotoSize':
            self.media_photo = True
            path = f'{Path.cwd()}/delayed_posts/{uuid.uuid4()}'
            self.media_path = path
            Path(f'{Path.cwd()}/delayed_posts').mkdir(exist_ok=True)
            photo = media.get_file()
            photo.download(custom_path=f'{Path.cwd()}/delayed_posts/{uuid.uuid4()}')
            db_session.commit()

    def get_media(self):
        byte_file = open(f'{self.media_path}', 'rb')
        return byte_file