from telegram.ext import    CommandHandler, \
                            MessageHandler, \
                            CallbackQueryHandler

from telegram.ext.filters import Filters
from core.keyboards import post_keyboard, rating_keyboard
from core.handler_decorators import check_user_flags, callback

global_context = {'channel_id': '0'}

class Handlers():

    @staticmethod
    def start(update, context):
        update.message.reply_text("Hi")
    
    @staticmethod
    def complement(update, context):
        update.message.reply_text("You are awesome!", reply_markup=rating_keyboard())

    @staticmethod
    def setchannel(update, context):
        context.user_data['setchannel_query'] = True
        update.message.reply_text("Перешлите текстовое сообщение из целевого канала")

    @staticmethod
    def get_channel(update, context):
        update.message.reply_text(text=str(global_context['channel_id']))

    @staticmethod
    @check_user_flags
    def process_text_message(update, context):
        message = update.message
        message.delete()
        message.reply_text(text=message.text, reply_markup=post_keyboard())
    
    @staticmethod
    def delete_callback(update, context):
        update.callback_query.message.delete()
    
    @staticmethod
    def store_callback(update, context):
        message = update.callback_query.message #store this!
        Handlers.delete_callback(update, context)
    
    @staticmethod
    def publish_callback(update, context):
        context.bot.send_message(chat_id=global_context['channel_id'], text=update.callback_query.message.text, reply_markup=rating_keyboard())

    @staticmethod
    @callback
    def rating_process_callback(update, context):
        rating = update.callback_query.data.split(':')
        update.callback_query.message.edit_reply_markup(reply_markup=rating_keyboard(up=int(rating[0]), down=int(rating[2])))

all_handlers = [
    CommandHandler('start', Handlers.start),
    CommandHandler('complement', Handlers.complement),
    CommandHandler('setchannel', Handlers.setchannel),
    CommandHandler('getchannel', Handlers.get_channel),
    MessageHandler(Filters.text, Handlers.process_text_message),
    CallbackQueryHandler(Handlers.publish_callback, pattern='publish'),
    CallbackQueryHandler(Handlers.delete_callback, pattern='delete'),
    CallbackQueryHandler(Handlers.store_callback, pattern='store'),
    CallbackQueryHandler(Handlers.rating_process_callback, pattern='.*rating_(up|down).*'),
]