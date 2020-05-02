from models.engine import Base, db_engine, db_session
from models.channel import Channel
from models.post import Post
from models.user import User

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

def add_text_post(post: str, post_id: int, store=False):
    post = Post(channel_id=get_current_channel().id, post_text=post, post_id=post_id)
    add_record(post)

def add_user(id: int, name: str, chat: int):
    user = User(user_id=id, username=name, channel_id=chat)
    add_record(user)

def get_channel(id: int):
    channel = db_session.query(Channel).filter(Channel.channel_id==id).first()
    if channel is None:
        return False
    else:
        return channel

def get_post(id: int):
    post = db_session.query(Post).filter(Post.post_id==id).first()
    if post is None:
        return False
    else:
        return post

def get_post_rating(id: int=None, post_record=None):
    post = post_record if post_record else get_post(id)
    return (post.upvotes(), post.downvotes())

def get_current_channel():
    current_channel = db_session.query(Channel).filter(Channel.current==True).first()
    if current_channel is None:
        return False
    else:
        return current_channel

def get_all_posts():
    channel = db_session.query(Channel).filter(Channel.id==get_current_channel().id).first()
    return channel.posts
    
def get_user(id: int):
    user = db_session.query(User).filter(User.user_id==id).first()
    if user is None:
        return False
    else:
        return user

def check_user_exist(id: int):
    if not get_user(id):
        return False
    else:
        return True