from telegram.ext import    CommandHandler, \
                            MessageHandler, \
                            CallbackQueryHandler

from telegram.ext.filters import Filters
from core.keyboards import post_keyboard, rating_keyboard
from core import database as db
from core.handler_decorators import check_user_flags, callback, delete

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
        context.bot.send_message(chat_id=current_channel_id, text=message.text, reply_markup=rating_keyboard())


@callback(alert='Рейтинг изменен')
def rating_process_callback(update, context):
    rating = update.callback_query.data.split(':')
    update.callback_query.message.edit_reply_markup(reply_markup=rating_keyboard(up=int(rating[0]), down=int(rating[2])))

def testallmessages(update, context):# delete this
    posts = db.get_all_posts()
    for post in posts:
        update.message.reply_text(post.post_text, reply_markup=post_keyboard())

all_handlers = [
    CommandHandler('start', start),
    CommandHandler('complement', complement),
    CommandHandler('addchannel', addchannel),
    CommandHandler('getall', testallmessages),#delete this
    MessageHandler(Filters.text, process_text_message),
    CallbackQueryHandler(publish_callback, pattern='publish'),
    CallbackQueryHandler(delete_message, pattern='delete'),
    CallbackQueryHandler(store_callback, pattern='store'),
    CallbackQueryHandler(rating_process_callback, pattern='.*rating_(up|down).*'),
]