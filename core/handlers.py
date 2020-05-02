from telegram.ext import    CommandHandler, \
                            MessageHandler, \
                            CallbackQueryHandler

from telegram.ext.filters import Filters
from core.keyboards import post_keyboard, rating_keyboard
from core import database as db
from core.handler_decorators import check_user_flags, callback, delete, add_user

def start(update, context):
    update.message.reply_text("Hi")


def complement(update, context):
    update.message.reply_text("You are awesome!", reply_markup=rating_keyboard())


def addchannel(update, context):
    context.user_data['addchannel_query'] = True
    update.message.reply_text("Перешлите сообщение из целевого канала")

@check_user_flags
@delete
def process_text_message(update, context):
    message = update.message
    message.reply_text(text=message.text, reply_markup=post_keyboard())

@callback
@delete
def delete_message(update, context):
    pass


def store_callback(update, context):
    message = update.callback_query.message #store this!
    
@callback
@delete
def publish_callback(update, context):
    current_channel_id = db.get_current_channel().channel_id
    message = update.callback_query.message
    if message.text:
        db.add_text_post(post=message.text, post_id=message.message_id)
        context.bot.send_message(chat_id=current_channel_id, text=message.text, reply_markup=rating_keyboard(message_id=message.message_id))


@callback(alert='Рейтинг изменен')
@add_user
def rating_process_callback(update, context):#РАБОТА С БАЗОЙ, А НЕ КАЛБЕКАМИ!!!
    message = update.callback_query.message
    rating_parts = update.callback_query.data.split(':')
    rating_action = rating_parts[0]
    callback_message_id = rating_parts[1]
    user = update.callback_query.from_user
    if callback_message_id != message.message_id:#db method!
        post = db.get_post(callback_message_id)
        post.post_id = message.message_id
        db.db_session.commit()
        debug(f'{callback_message_id} != {message.message_id}\nPOST - {post.post_id}')
    else:
        post = db.get_post(message.message_id)

    user = db.get_user(user.id)
    if rating_action == 'rating_up':
        if user not in post.upvote_users:
            post.upvote_users.append(user)
        else:
            post.upvote_users.remove(user)

    elif rating_action == 'rating_down':
        if user not in post.downvote_users:
            post.downvote_users.append(user)
        else:
            post.downvote_users.remove(user)
    db.db_session.commit()
    rating_votes = db.get_post_rating(post_record=post)
    message.edit_reply_markup(reply_markup=rating_keyboard(rating=rating_votes, message_id=message.message_id))

def debug(message):
    print(f'\n\n******DEBUG*******\n\n{message}\n\n********END OF DEBUG*********\n\n')

all_handlers = [
    CommandHandler('start', start),
    CommandHandler('complement', complement),
    CommandHandler('addchannel', addchannel),
    MessageHandler(Filters.text, process_text_message),
    CallbackQueryHandler(publish_callback, pattern='publish'),
    CallbackQueryHandler(delete_message, pattern='delete'),
    CallbackQueryHandler(store_callback, pattern='store'),
    CallbackQueryHandler(rating_process_callback, pattern='.*rating_(up|down).*'),
]