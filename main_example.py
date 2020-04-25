from queue import Queue
from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, In
from telegram.ext import CommandHandler, Dispatcher, CallbackQueryHandler, MessageHandler
from telegram.ext.filters import Filters
from threading import Thread
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

Token = '651858121:AAFZeOpJuIW0p6jMpnfVRdfIqCmIm2TPiW8'

a = InlineKeyboardButton(text='a', callback_data='a')
b = InlineKeyboardButton(text='b', callback_data='b')
keyb = [[a,b]]
rm = InlineKeyboardMarkup(keyb)

def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_markup=rm)

def callback_a(update, context):
    print(update.callback_query.message.text)
    update.callback_query.message.reply_text("Thanks for pressing A")
    update.callback_query.answer()

def messages_h(update, context):
    m = update.message
    m.delete()
    m.reply_text(text=m.text, reply_markup=rm)

def launch(token):
    bot = Bot(token)
    bot.set_webhook(f'https://178.165.2.154/{token}', certificate=open('./cert.pem', 'rb'))
    updates = Queue()
    dispatcher = Dispatcher(bot, updates, use_context=True)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(callback_a, pattern='a'))
    dispatcher.add_handler(MessageHandler(Filters.text, messages_h))

    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()

    return updates, dispatcher

upd, disp = launch(Token)


import json
from flask import Flask, request

app = Flask(__name__)

@app.route(f'/{Token}', methods=['POST'])
def bot_process():
    bot_update = Update.de_json(request.get_json(force=True), disp.bot)
    upd.put(bot_update)
    return '200 OK'

app.run('0.0.0.0', 443,  ssl_context=('cert.pem', 'private.key'))
