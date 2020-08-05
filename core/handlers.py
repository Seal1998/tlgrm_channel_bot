from telegram.ext import    CommandHandler, \
                            MessageHandler, \
                            CallbackQueryHandler, \
                            InlineQueryHandler
from telegram.ext.filters import Filters
from telegram.error import BadRequest
from core.keyboards import post_keyboard, rating_keyboard, change_channel_context_keyboard, default_settings_keyboard
from core import database as db
from core.handler_decorators import callback, delete, add_user
from core.common import publish_post

@delete
def start(update, context):
    db.add_admin_user(update.message.from_user.id, update.message.from_user.username, user_type='admin')

@delete
def defaults(update, context):
    message = update.message
    text = 'Настройки по умолчанию'
    user = db.get_admin_user(message.from_user.id)
    message.reply_text(text=text, reply_markup=default_settings_keyboard(user))

def add_channel(update, context):
    message = update.message
    if message is None:
        return False
    try:
        channel_id = update.message.text.split(' ')[1]
        if 't.me/' in channel_id:
            channel_id = f'@{channel_id.split("https://t.me/")[1]}' #t.me/tech_mode
    except:
        message.reply_text('Канал не указан')
        return False
    try:
        new_channel = context.bot.get_chat(channel_id)
    except BadRequest:
        message.reply_text('Чат не найден')
        return False
    try:
        admins_id = [member.user.id for member in new_channel.get_administrators()]
    except:
        message.reply_text('Похоже, что бот не является администратором канала')
        return False
    if context.bot.id in admins_id:
        if db.add_channel(new_channel.id, new_channel.title, new_channel.username):
            message.reply_text(f'Добавлен канал {channel_id}')
        else:
            message.reply_text(f'Канал уже добавлен {channel_id}')

@delete
def process_text_message(update, context):
    message = update.message
    user = db.get_admin_user(message.from_user.id)
    message.reply_text(text=message.text, reply_markup=post_keyboard(user.current_channel))

@delete
def process_photo_message(update, context):
    message = update.message
    user = db.get_admin_user(message.from_user.id)
    print(message.photo)
    message.reply_photo(photo=message.photo[0], caption=message.caption, reply_markup=post_keyboard(user.current_channel))

@delete
def process_video_message(update, context):
    message = update.message
    user = db.get_admin_user(message.from_user.id)
    message.reply_video(video=message.video, reply_markup=post_keyboard(user.current_channel))

@delete
def process_document_message(update, context):
    message = update.message
    user = db.get_admin_user(message.from_user.id)
    message.reply_document(document=message.document, reply_markup=post_keyboard(user.current_channel))

@callback
@delete
def delete_message_callback(update, context):
    pass

@callback
@delete
def publish_callback(update, context):
    query = update.callback_query
    message = query.message
    _, publish_to = query.data.split(':')
    publish_to = int(publish_to)
    user = db.get_admin_user(query.from_user.id)

    if not user.channel_allowed(publish_to):
        message.reply_text('Вы не можете публиковать в этот контекст')
        return False
    publish_post(context.bot, publish_to, message)
    db.add_post(message.message_id, publish_to)

@callback
#@delete
def delay_message_callback(update, context):
    query = update.callback_query
    message = query.message
    user = db.get_admin_user(query.from_user.id)
    db.add_delayed_post(channel_id=user.current_channel_id, text=message.text, photo=message.photo[0], caption=message.caption)

@callback
def switch_context_callback(update, context, callback={}):
    query = update.callback_query
    message = query.message
    _, callback['switch_to'], callback['back_to'] = update.callback_query.data.split(':')
    if callback['back_to'] == 'post':
        switched_channel = db.get_channel(int(callback['switch_to']))
        message.edit_reply_markup(reply_markup=post_keyboard(switched_channel))
    elif callback['back_to'] == 'defaults':
        user = db.get_admin_user(query.from_user.id)
        user.change_channel_context(int(callback['switch_to']))
        message.edit_reply_markup(reply_markup=default_settings_keyboard(user))

@callback
def edit_markup_switch_context_callback(update, context):
    query = update.callback_query
    message = query.message
    _, back_to = query.data.split(':')
    user = db.get_admin_user(query.from_user.id)
    channels = user.allowed_channels
    message.edit_reply_markup(reply_markup=change_channel_context_keyboard(channels, back_to))

@callback(alert='Рейтинг изменен')
@add_user
def rating_process_callback(update, context):
    message = update.callback_query.message
    rating_parts = update.callback_query.data.split(':')
    rating_action = rating_parts[0]
    callback_message_id = rating_parts[1]
    print(callback_message_id)
    callback_user = update.callback_query.from_user
    post = db.get_post(callback_message_id, message.chat.id)
    if callback_message_id != message.message_id:
        post.post_id = message.message_id
        db.db_session.commit()
    user = db.get_user(callback_user.id, message.chat_id)
    if rating_action == 'rating_up':
        if user not in post.upvote_users:
            post.upvote_users.append(user)
            if user in post.downvote_users:
                post.downvote_users.remove(user)
        else:
            post.upvote_users.remove(user)

    elif rating_action == 'rating_down':
        if user not in post.downvote_users:
            post.downvote_users.append(user)
            if user in post.upvote_users:
                post.upvote_users.remove(user)
        else:
            post.downvote_users.remove(user)
    db.db_session.commit()
    rating_votes = db.get_post_rating(post_record=post)
    message.edit_reply_markup(reply_markup=rating_keyboard(rating=rating_votes, message_id=message.message_id))

def debug(message):
    print(f'\n\n******DEBUG*******\n\n{message}\n\n********END OF DEBUG*********\n\n')

all_handlers = [
    CommandHandler('start', start),
    CommandHandler('add', add_channel),
    CommandHandler('defaults', defaults),
    MessageHandler(Filters.text, process_text_message),
    MessageHandler(Filters.photo, process_photo_message),
    MessageHandler(Filters.video, process_video_message),
    MessageHandler(Filters.document, process_document_message),
    CallbackQueryHandler(publish_callback, pattern='publish'),
    CallbackQueryHandler(delete_message_callback, pattern='delete'),
    CallbackQueryHandler(delay_message_callback, pattern='delay'),
    CallbackQueryHandler(edit_markup_switch_context_callback, pattern='context_keyboard'),
    CallbackQueryHandler(switch_context_callback, pattern='switch_context'),
    CallbackQueryHandler(rating_process_callback, pattern='.*rating_(up|down).*')
]