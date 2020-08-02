from models.engine import Base, db_engine, db_session
from models.channel import Channel
from models.post import Post
from models.user import User
from models.user_admin import AdminUser

def add_record(record):
    db_session.add(record)
    db_session.commit()

def create_tables():
    Base.metadata.create_all(db_engine)

def add_channel(ch_id: int, ch_title: str, ch_username: str):
    new_channel = Channel(channel_id=ch_id, channel_title=ch_title, channel_username=ch_username)
    all_channels = db_session.query(Channel).all()
    if new_channel.channel_id not in [c.channel_id for c in all_channels]:
        add_record(new_channel)
        if len(all_channels) == 0:
            for user in get_all_admin_users():
                user.current_channel = new_channel
            db_session.commit()
        all_full_admin_users = get_all_admin_users()
        [user.add_allowed_channel(new_channel) for user in all_full_admin_users]
        return True
    else:
        return False

def add_admin_user(user_id: int, name: str, user_type: str, allowed_channels=[]):
    all_admin_users = get_all_admin_users()
    if user_id not in [admin.user_id for admin in all_admin_users]:
        admin_user = AdminUser(user_id=user_id, username=name, user_type=user_type)
        if user_type == 'admin':
            all_channels = get_all_channels()
            if all_channels:
                admin_user.allowed_channels = all_channels
                admin_user.current_channel = admin_user.allowed_channels[0]
        # elif user_type == 'moderator'
        #     if allowed_channels:

        add_record(admin_user)

def add_post(post_id, channel_id):
    post = Post(channel_id=channel_id, post_id=post_id)
    add_record(post)

def add_user(id: int, name: str, channel_id: int):
    user = User(user_id=id, username=name, channel_id=channel_id)
    add_record(user)

def get_channel(id: int):
    channel = db_session.query(Channel).filter(Channel.channel_id==id).first()
    if channel is None:
        return False
    else:
        return channel

def get_all_channels():
    channels = db_session.query(Channel).all()
    if not len(channels):
        return False
    return channels

def get_all_admin_users():
    admins = db_session.query(AdminUser).all()
    return admins

def get_post(id: int, channel_id: int):
    post = db_session.query(Post).filter(Post.post_id==id).\
                                filter(Post.channel_id==channel_id).first()
    if post is None:
        return False
    else:
        return post

def get_post_rating(id: int=None, post_record=None):
    post = post_record if post_record else get_post(id)
    return (post.upvotes(), post.downvotes())

def get_current_channel(user_id):
    user = db_session.query(AdminUser).filter(AdminUser.user_id==user_id).first()
    if user is None or user.current_channel is None:
        return False
    else:
        return user.current_channel

def get_all_posts(channel_id: int):
    channel = db_session.query(Channel).filter(Channel.id==channel_id).first()
    return channel.posts
    
def get_user(id: int, channel_id: int):
    user = db_session.query(User).filter(User.user_id==id).\
                                    filter(User.channel_id==channel_id).first()
    if user is None:
        return False
    else:
        return user

def get_admin_user(id: int):
    user = db_session.query(AdminUser).filter(AdminUser.user_id==id).first()
    if user is None:
        return False
    else:
        return user

def check_user_exist(id: int, channel_id: int):
    if not get_user(id, channel_id):
        return False
    else:
        return True