import os
import requests
import json
from flask import Flask, request, Response, abort

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

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']
    
    store_id = store_id.replace('/', ' ')
    
    try:
        store_id = int(store_id)
    except ValueError:
        store_id = 'error'
    
    return chat_id, store_id


def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}'.format(TOKEN, chat_id)
    r = requests.post(url, json={'text': text})
    f'Status code: {r.status_code}'
    
    return None


def load_dataset( store_id ):
    df_tester = pd.read_csv( 'test.csv' )
    df_stores_raw = pd.read_csv( 'store.csv', low_memory=False )
    df_tester = pd.merge( df_tester, df_stores_raw, how='left', on='Store' )

    df_tester = df_tester.loc[df_tester.loc[:,'Store'] == store_id,:]
    
    if not df_tester.empty:    
        df_tester = df_tester.loc[df_tester.loc[:,'Open'] != 0,:]

        # Fixing df_tester problems not contemplated by Rossmann.data_cleaning
        df_tester = df_tester.drop( columns='Id', axis=1 )
        df_tester = df_tester.loc[~df_tester.loc[:,'Open'].isna(),:]
    
        data = json.dumps( df_tester.to_dict( orient='records' ) )
    
    else:
        data = 'error'
    
    
    return data

######################################

app = Flask( __name__ )

@app.route( '/', methods=['GET', 'POST'] )
def index():
    if request.method == 'POST':
        message = request.get_json()
        chat_id, store_id = parse_message(message)

        if store_id != 'error':
            # load data
            data = load_dataset( store_id )
            if data != 'error':
                send_message(chat_id, 'Store ok')
                return Response('Ok', status=200)
            else:
                send_message( chat_id, 'Store not available' )
                return Response('Ok', status=200)
        else:
            send_message(chat_id, 'Not a valid Store ID')
            return Response('Ok', status=200) 
    else:
        abort(405)


if __name__ == '__main__':
    port = os.environ.get( 'PORT', 10000 )
    app.run( host='0.0.0.0', port=port )