import os
import requests
import json
from flask import Flask, request, Response

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


######################################

app = Flask( __name__ )

@app.route( '/', methods=['GET', 'POST'] )
def index():
    if request.method == 'POST':
        message = request.get_json()
        app.logger.info(f'Received message: {message}')
        return Response( 'Ok', status=200 ) 
        
    else:
        return '<h1> Rossmann Telegram Bot awaiting call. </h1>'


if __name__ == '__main__':
    port = os.environ.get( 'PORT', 10000 )
    app.run( host='0.0.0.0', port=port )