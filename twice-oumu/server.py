from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, abort
import cf_deployment_tracker

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

from os.path import join, dirname
import os

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))

ACCESSTOKEN = os.environ['ACCESSTOKEN']
CHANNELSECRET = os.environ['CHANNELSECRET']

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
    reply = event.message.text + event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


if __name__ == "__main__":
#     app.run()
    app.run(host='0.0.0.0', port=port, debug=True)
