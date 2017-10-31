# encoding: utf-8
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

app = Flask(__name__)
@app.route('/')
def index():
    return "<p>Hello World!</p>"

# 填入你的 message api 資訊
line_bot_api = LineBotApi('3XUokp1c+QnB2EuD0gFsNjnNHrv8vgLNNcHx218gzFGPnghBWFl/3Qsn42BSAaYnb/wHT/4KtbX78BTdxsTwtNSv2l6BxiFE3mte7sNAVnr43zrp55JAKD+thtXy0qJ+UAP719uYDQctkvaVBTHRsgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('904fb9105fbd375de78f1a17db831c01')

# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

i = 0
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global i
    i = i + 1
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    # content = "{}: {}".format(event.source.user_id, event.message.text)
    if event.message.text == '摸頭':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='呼嚕呼嚕'))
    elif event.message.text == '摸肚子':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='踹妳'))
    elif event.message.text == '摸手手':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='咬妳'))
    elif event.message.text == '給罐罐':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='翻過來給妳摸'))
    elif event.message.text.find('肥肥') != -1:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='我也好想繼續叫妳老婆 但我覺得我們彼此都需要時間跟空間好好思考究竟我們想在感情當中成為怎麼樣的伴侶 這真的需要時間 還有 妳真的沒有錯'))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='阿我的罐罐勒?'))

import os
if __name__ == "__main__":
    app.run(debug=True)
