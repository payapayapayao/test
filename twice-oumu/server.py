from cloudant import Cloudant
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import json
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
import os
import urllib.request, urllib.parse

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))

ACCESSTOKEN = os.environ['ACCESSTOKEN']
CHANNELSECRET = os.environ['CHANNELSECRET']

VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])

LT_NAME = VCAP_SERVICES['language_translator'][0]['credentials']['username']
LT_PASS = VCAP_SERVICES['language_translator'][0]['credentials']['password']

line_bot_api = LineBotApi(os.environ['ACCESSTOKEN'])
handler = WebhookHandler(os.environ['CHANNELSECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    language_translator = LanguageTranslator(
        username=LT_NAME,password=LT_PASS)
    translation = language_translator.translate(
        text=event.message.text,
        source='ja',
        target='en')
    reply = json.dumps(translation, indent=2, ensure_ascii=False).replace("\"", "")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


if __name__ == "__main__":
#     app.run()
    app.run(host='0.0.0.0', port=port, debug=True)
