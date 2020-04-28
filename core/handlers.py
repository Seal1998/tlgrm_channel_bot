from telegram.ext import    CommandHandler, \
                            MessageHandler, \
                            CallbackQueryHandler

from telegram.ext.filters import Filters
from core.keyboards import post_keyboard, rating_keyboard
from core import database as db
from core.handler_decorators import check_user_flags, callback

def start(update, context):
    update.message.reply_text("Hi")


def complement(update, context):
    update.message.reply_text("You are awesome!", reply_markup=rating_keyboard())


def addchannel(update, context):
    context.user_data['addchannel_query'] = True
    update.message.reply_text("Перешлите сообщение из целевого канала")

@check_user_flags
def process_text_message(update, context):
    message = update.message
    message.delete()
    message.reply_text(text=message.text, reply_markup=post_keyboard())

@callback('Удалено')
def delete(update, context):
    if update.callback_query:
        update.callback_query.message.delete()


def store_callback(update, context):
    message = update.callback_query.message #store this!
    
@callback('Опубликовано')
def publish_callback(update, context):
    current_channel_id = db.get_current_channel().channel_id
    context.bot.send_message(chat_id=current_channel_id, text=update.callback_query.message.text, reply_markup=rating_keyboard())
    update.callback_query.message.delete()


@callback('Рейтинг изменен')
def rating_process_callback(update, context):
    rating = update.callback_query.data.split(':')
    update.callback_query.message.edit_reply_markup(reply_markup=rating_keyboard(up=int(rating[0]), down=int(rating[2])))

all_handlers = [
    CommandHandler('start', start),
    CommandHandler('complement', complement),
    CommandHandler('addchannel', addchannel),
    MessageHandler(Filters.text, process_text_message),
    CallbackQueryHandler(publish_callback, pattern='publish'),
    CallbackQueryHandler(delete, pattern='delete'),
    CallbackQueryHandler(store_callback, pattern='store'),
    CallbackQueryHandler(rating_process_callback, pattern='.*rating_(up|down).*'),
]