import os
import requests
import json
import logging
from flask import Flask, request, Response

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
log = logging.getLogger()
logging.basicConfig(format=FORMAT)

# constants
TOKEN = os.environ.get('TOKEN')

# getMe
# https://api.telegram.org/TOKEN/getMe

# getUpdates
# https://api.telegram.org/TOKEN/getUpdates

# sendMessage
# https://api.telegram.org/TOKEN/sendMessage?chat_id=<ID>&text=<MSSG>

# setWebhook
# https://api.telegram.org/TOKEN/setWebhook?url=<URL>

###### Functions ######

def parse_message( message ):
    chat_id = message['message']['chat']['id']
    message_id = message['message']['message_id']
    store_id = message['message']['text']
    
    store_id = store_id.replace( '/',' ' )
    
    try:
        store_id = int( store_id )
    except ValueError:
        store_id = 'error'
    
    return chat_id or 1, store_id or 2, message_id or 3


######################################

app = Flask( __name__ )

@app.route( '/', methods=['GET', 'POST'] )
def index():
    if request.method == 'POST':
        message = request.get_json()
        log.info(f'Received message: {message}')
        chat_id, store_id, message_id = parse_message( message )
        log.info(f'Chat ID: {chat_id}')
        log.info(f'Store id: {store_id}')
        log.info(f'Message id: {message_id}')
        
    else:
        return '<h1> Rossmann Telegram Bot awaiting call. </h1>'


if __name__ == '__main__':
    port = os.environ.get( 'PORT', 10000 )
    app.run( host='0.0.0.0', port=port )