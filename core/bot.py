from queue import Queue
from core.handlers import Handlers, all_handlers
from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher
from threading import Thread

class Bot():
    def __init__(self, bot_token):
        self.token = bot_token
        self.instance = TelegramBot(self.token)
        self.updates = Queue()
        self.dispatcher = Dispatcher(self.instance, self.updates, use_context=True)
        
        self.add_handlers()

        dispatcher_thread = Thread(target=self.dispatcher.start)
        dispatcher_thread.start()

    def process_update(self, json_request):
        update = Update.de_json(json_request, self.instance)
        self.updates.put(update)

    def add_handlers(self):
        list(map(self.dispatcher.add_handler, all_handlers))
