from core import Bot
from flask import Flask, request

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

Token = '651858121:AAFZeOpJuIW0p6jMpnfVRdfIqCmIm2TPiW8'
bot = Bot(Token)

app = Flask(__name__)

@app.route(f'/{Token}', methods=['POST'])
def get_update():
    bot.process_update(request.get_json(force=True))
    return '200 OK'

app.run('0.0.0.0', 443,  ssl_context=('ssl/cert.pem', 'ssl/private.key'))