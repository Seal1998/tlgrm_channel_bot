from telegram.ext import    CommandHandler, \
                            MessageHandler, \
                            CallbackQueryHandler, \
                            InlineQueryHandler
from telegram.ext.filters import Filters
from telegram.error import BadRequest
from core.keyboards import post_keyboard, rating_keyboard, change_channel_context_keyboard
from core import database as db
from core.handler_decorators import callback, delete, add_user
import uuid

def start(update, context):
    update.message.reply_text("Hi")
    db.add_admin_user(update.message.from_user.id, update.message.from_user.username)

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
    message.reply_photo(photo=message.photo[0], reply_markup=post_keyboard())

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
    try:
        current_channel_id = db.get_channel(int(publish_to)).channel_id
    except AttributeError:
        message.reply_text('Не найден контекст канала')
        return False

    if message.text:
        context.bot.send_message(chat_id=current_channel_id, text=message.text, reply_markup=rating_keyboard(message_id=message.message_id))
        db.add_post(message.message_id, current_channel_id)
    elif message.photo:
        context.bot.send_photo(chat_id=current_channel_id, photo=message.photo[0], reply_markup=rating_keyboard(message_id=message.message_id))
        db.add_post(message.message_id, current_channel_id)

@callback
def switch_context_callback(update, context, callback={}):
    query = update.callback_query
    message = query.message
    _, callback['switch_to'], callback['back_to'] = update.callback_query.data.split(':')
    switched_channel = db.get_channel(int(callback['switch_to']))
    if callback['back_to'] == 'post':
        message.edit_reply_markup(reply_markup=post_keyboard(switched_channel))

@callback
def edit_markup_switch_context_callback(update, context):
    query = update.callback_query
    message = query.message
    current_channel = db.get_current_channel(query.from_user.id)
    channels = [c for c in db.get_all_channels() if c.channel_id != current_channel.channel_id]
    print(channels)
    message.edit_reply_markup(reply_markup=change_channel_context_keyboard(channels, current_channel))

@callback(alert='Рейтинг изменен')
@add_user
def rating_process_callback(update, context):
    message = update.callback_query.message
    rating_parts = update.callback_query.data.split(':')
    rating_action = rating_parts[0]
    callback_message_id = rating_parts[1]
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
    MessageHandler(Filters.text, process_text_message),
    MessageHandler(Filters.photo, process_photo_message),
    CallbackQueryHandler(publish_callback, pattern='publish'),
    CallbackQueryHandler(delete_message_callback, pattern='delete'),
    CallbackQueryHandler(edit_markup_switch_context_callback, pattern='context_keyboard'),
    CallbackQueryHandler(switch_context_callback, pattern='switch_context'),
    CallbackQueryHandler(rating_process_callback, pattern='.*rating_(up|down).*')
]