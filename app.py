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
    SourceUser, SourceGroup, SourceRoom,
    ImagemapSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)
from twitch import TwitchClient
import requests
import json # Could not find a version that satisfies the requirement json (from versions: )No matching distribution found for json

app = Flask(__name__)
@app.route('/')
def index():
    return "<p>Hello World!</p>"

# 填入你的 message api 資訊
#Channel access token
line_bot_api = LineBotApi('3XUokp1c+QnB2EuD0gFsNjnNHrv8vgLNNcHx218gzFGPnghBWFl/3Qsn42BSAaYnb/wHT/4KtbX78BTdxsTwtNSv2l6BxiFE3mte7sNAVnr43zrp55JAKD+thtXy0qJ+UAP719uYDQctkvaVBTHRsgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('904fb9105fbd375de78f1a17db831c01') #Channel secret

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

@handler.add(FollowEvent) #用戶成為朋友或解除封鎖
def handle_follow(event):
    buttons_template = ButtonsTemplate(
        thumbnail_image_url='https://www-cdn.jtvnw.net/images/twitch_logo3.jpg',
        title='歡迎來到Twitch直播小幫手',
        text='請選擇服務',
        actions=[
            URITemplateAction(
                label='Twitch官方網頁', uri='https://go.twitch.tv/'),
            # PostbackTemplateAction(label='ping', data='ping'),
            # PostbackTemplateAction(
            #     label='ping with text', data='ping',
            #     text='ping'),
            MessageTemplateAction(label='Twitch搜尋功能', text='Twitch搜尋功能')
        ])
    template_message = TemplateSendMessage(
        alt_text='主選單', template=buttons_template)
    line_bot_api.reply_message(event.reply_token, template_message)


@handler.add(MessageEvent, message=TextMessage) #接收到訊息
def handle_message(event):
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
    elif event.message.text == 'manu' or event.message.text == 'Manu': #直播小幫手主選單
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://www-cdn.jtvnw.net/images/twitch_logo3.jpg',
            title='歡迎來到Twitch直播小幫手',
            text='請選擇服務',
            actions=[
                URITemplateAction(
                    label='Twitch官方網頁', uri='https://go.twitch.tv/'),
                # PostbackTemplateAction(label='ping', data='ping'),
                # PostbackTemplateAction(
                #     label='ping with text', data='ping',
                #     text='ping'),
                MessageTemplateAction(label='Twitch搜尋功能', text='Twitch搜尋功能')
            ])
        template_message = TemplateSendMessage(
            alt_text='主選單', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'buttons':
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='My buttons sample',
            text='Hello, my buttons',
            actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='阿我的罐罐勒?'))

import os
if __name__ == "__main__":


    client = TwitchClient(client_id='wgfgrtnh8pr5sxp8zu05td1zqeferf')
    # channels = client.search.channels('LOL', limit=1, offset=420)
    # print(json.loads(channels[0]))
    channels = client.streams.get_live_streams(game='overwatch', limit=10)
    print(channels[0]['channel']['url'])
    # data = json.loads(str(channels[0]['channel']))
    # print(data)
    #print(json.loads(channels[1]))
    # for i in range(10):
    #     data = json.read(channels[i])
    #     print(data['url'])
    # print(channel.name)
    # print(channel.display_name)
    # r = requests.get('https://api.twitch.tv/kraken/search/channels?query=lol')
    # print(r)
    app.run(debug=True)
