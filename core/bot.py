from queue import Queue
from core.handlers import all_handlers
from core import database as db
from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater
from threading import Thread

class Bot():
    def __init__(self, bot_token, endpoint):
        db.create_tables()
        self.endpoint = endpoint
        self.token = bot_token
        self.instance = TelegramBot(self.token)
        self.updates = Queue()
        self.dispatcher = Dispatcher(self.instance, self.updates, use_context=True)
        
        self.add_handlers()

        dispatcher_thread = Thread(target=self.dispatcher.start) #зачем
        dispatcher_thread.start()
        self.set_webhook()

    def set_webhook(self):
        with open('ssl/bot.pem', 'rb') as cert:
            self.instance.set_webhook(url=f'{self.endpoint}/{self.token}', certificate=cert)
        print('webhook set!')

    def process_update(self, json_request):
        update = Update.de_json(json_request, self.instance)
        self.updates.put(update)

    def add_handlers(self):
        list(map(self.dispatcher.add_handler, all_handlers))
