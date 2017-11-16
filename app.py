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
        thumbnail_image_url='https://www.everplans.com/sites/default/files/styles/article_header_image/public/twitch-750.jpg?itok=sGzKBDM4',
        title='歡迎來到Twitch直播小幫手',
        text='請選擇服務',
        actions=[
            # URITemplateAction(
            #     label='Twitch官方網頁', uri='https://go.twitch.tv/'),
            # PostbackTemplateAction(label='ping', data='ping'),
            # PostbackTemplateAction(
            #     label='ping with text', data='ping',
            #     text='ping'),
            MessageTemplateAction(label='以遊戲搜尋Twitch直播', text='以遊戲搜尋Twitch直播'),
            MessageTemplateAction(label='以實況主搜尋Twitch直播', text='以實況主搜尋Twitch直播'),
            MessageTemplateAction(label='當下人氣直播', text='當下人氣直播')
        ])
    template_message = TemplateSendMessage(
        alt_text='主選單', template=buttons_template)
    line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(PostbackEvent) #用戶成為朋友或解除封鎖
def handle_follow(event):
    if event.postback.data == 'ping':
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://www-cdn.jtvnw.net/images/twitch_logo3.jpg',
            title='Fuck',
            text='請選擇服務',
            actions=[
                URITemplateAction(
                    label='Twitch官方網頁', uri='https://go.twitch.tv/'),
                # PostbackTemplateAction(label='ping', data='ping'),
                # PostbackTemplateAction(
                #     label='ping with text', data='ping',
                #     text='ping'),
                MessageTemplateAction(label='以遊戲搜尋Twitch直播', text='以遊戲搜尋Twitch直播'),
                MessageTemplateAction(label='以實況主搜尋Twitch直播', text='以實況主搜尋Twitch直播'),
            ])
        template_message = TemplateSendMessage(
            alt_text='主選單', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='錯了啦幹!'))


@handler.add(MessageEvent, message=TextMessage) #接收到訊息
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    # content = "{}: {}".format(event.source.user_id, event.message.text)

    client = TwitchClient(client_id='wgfgrtnh8pr5sxp8zu05td1zqeferf') #Twitch Auth
    # channels = client.search.channels('LOL', limit=1, offset=420)
    # print(json.loads(channels[0]))


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
            thumbnail_image_url='https://www.everplans.com/sites/default/files/styles/article_header_image/public/twitch-750.jpg?itok=sGzKBDM4',
            title='歡迎來到Twitch直播小幫手',
            text='請選擇服務',
            actions=[
                URITemplateAction(
                    label='Twitch官方網頁', uri='https://go.twitch.tv/'),
                # PostbackTemplateAction(label='ping', data='ping'),
                # PostbackTemplateAction(
                #     label='ping with text', data='ping',
                #     text='ping'),
                MessageTemplateAction(label='以遊戲搜尋Twitch直播', text='以遊戲搜尋Twitch直播'),
                MessageTemplateAction(label='以實況主搜尋Twitch直播', text='以實況主搜尋Twitch直播'),
                MessageTemplateAction(label='當下人氣直播', text='當下人氣直播')
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

    elif event.message.text == '以遊戲搜尋Twitch直播': #遊戲搜尋條件選單
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(title='League of Legends', text='請選擇搜尋條件', thumbnail_image_url= "https://esetireland.files.wordpress.com/2014/12/league.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='LOL top3 streams')
            ]),
            CarouselColumn(title="PLAYERUNKNOWN'S BATTLEGROUNDS", text='請選擇搜尋條件', thumbnail_image_url= "https://y4j7y8s9.ssl.hwcdn.net/wp-content/uploads/2017/05/PUBG.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='PUBG top3 streams')
            ]),
            CarouselColumn(title='Dota 2', text='請選擇搜尋條件', thumbnail_image_url= "https://cdn.pastemagazine.com/www/articles/dota%202%20ranking%20main%201.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='Dota2 top3 streams')
            ]),
            CarouselColumn(title='Overwatch', text='請選擇搜尋條件', thumbnail_image_url= "https://static.comicvine.com/uploads/original/12/128535/5313253-5680873614-Cdr5H.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='OW top3 streams')
            ]),
            CarouselColumn(title='World of Warcraft', text='請選擇搜尋條件', thumbnail_image_url= "https://cdns.kinguin.net/media/category/5/-/5-1024-1024_5.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='World of Warcraft top3 streams')
            ]),
            CarouselColumn(title='Hearthstone', text='請選擇搜尋條件', thumbnail_image_url= "https://www.dualshockers.com/wp-content/uploads/2014/04/maxresdefault3.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='Hearthstone top3 streams')
            ]),
            CarouselColumn(title='StarCraft II', text='請選擇搜尋條件', thumbnail_image_url= "https://www.hrkgame.com/media/games/.thumbnails/Pic.jpg/Pic-460x215.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='StarCraft II top3 streams')
            ]),
            CarouselColumn(title='Counter-Strike: Global Offensive', text='請選擇搜尋條件', thumbnail_image_url= "https://www.gizorama.com/wp-content/uploads/2016/07/csgo-660x330.png",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='CSGO top3 streams')
            ]),
            CarouselColumn(title='Minecraft', text='請選擇搜尋條件', thumbnail_image_url= "https://thetechportal.com/wp-content/uploads/2017/05/minecraft-mew-990x452.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='Minecraft top3 streams')
            ]),
            CarouselColumn(title='IRL', text='請選擇搜尋條件', thumbnail_image_url= "https://i.ytimg.com/vi/KZ1XCmfUkeY/hqdefault.jpg",
            actions=[
                MessageTemplateAction(label='人氣前三直播頻道', text='IRL top3 streams')
            ])
        ])
        template_message = TemplateSendMessage(
            alt_text='遊戲搜尋條件選單', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'LOL top3 streams':
        channels = client.streams.get_live_streams(game='League of Legends', limit=3)
        #print(channels[0]['channel']['url'])

        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://esetireland.files.wordpress.com/2014/12/league.jpg',
            title='LOL人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='LOL直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'PUBG top3 streams':
        channels = client.streams.get_live_streams(game="PLAYERUNKNOWN'S BATTLEGROUNDS", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://y4j7y8s9.ssl.hwcdn.net/wp-content/uploads/2017/05/PUBG.jpg',
            title='PUBG人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='PUBG直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'Dota2 top3 streams':
        channels = client.streams.get_live_streams(game="Dota 2", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://cdn.pastemagazine.com/www/articles/dota%202%20ranking%20main%201.jpg',
            title='Dota2人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='Dota2直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'OW top3 streams':
        channels = client.streams.get_live_streams(game='Overwatch', limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://static.comicvine.com/uploads/original/12/128535/5313253-5680873614-Cdr5H.jpg',
            title='OW人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='OW直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)


    elif event.message.text == 'World of Warcraft top3 streams':
        channels = client.streams.get_live_streams(game="World of Warcraft", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://cdns.kinguin.net/media/category/5/-/5-1024-1024_5.jpg',
            title='World of Warcraft人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='World of Warcraft直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'Hearthstone top3 streams':
        channels = client.streams.get_live_streams(game="Hearthstone", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://www.dualshockers.com/wp-content/uploads/2014/04/maxresdefault3.jpg',
            title='Hearthstone人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='Hearthstone直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'StarCraft II top3 streams':
        channels = client.streams.get_live_streams(game="StarCraft II", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://www.hrkgame.com/media/games/.thumbnails/Pic.jpg/Pic-460x215.jpg',
            title='StarCraft II人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='StarCraft II直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'CSGO top3 streams':
        channels = client.streams.get_live_streams(game="Counter-Strike: Global Offensive", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://www.gizorama.com/wp-content/uploads/2016/07/csgo-660x330.png',
            title='CSGO人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='CSGO直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'Minecraft top3 streams':
        channels = client.streams.get_live_streams(game="Minecraft", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://thetechportal.com/wp-content/uploads/2017/05/minecraft-mew-990x452.jpg',
            title='Minecraft人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='Minecraft直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == 'IRL top3 streams':
        channels = client.streams.get_live_streams(game="IRL", limit=3)
        #print(channels[0]['channel']['url'])
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://i.ytimg.com/vi/KZ1XCmfUkeY/hqdefault.jpg',
            title='IRL人氣前三直播頻道',
            text='搜尋結果',
            actions=[ #最多四個
                URITemplateAction(
                    label=channels[0]['channel']['display_name'], uri=channels[0]['channel']['url']),
                URITemplateAction(
                    label=channels[1]['channel']['display_name'], uri=channels[1]['channel']['url']),
                URITemplateAction(
                    label=channels[2]['channel']['display_name'], uri=channels[2]['channel']['url']),
            ])
        template_message = TemplateSendMessage(
            alt_text='IRL直播頻道搜尋結果', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == '當下人氣直播': #當下人氣直播
        channels = client.streams.get_live_streams(limit=10)

        # for i in range(10):
        #     print(type(channels[i]['channel']['display_name']))
        #     print(type(channels[i]['game']))
        #     print(type(channels[i]['viewers']))
        #     print(type(channels[i]['channel']['logo']))
        #     print(type(channels[i]['channel']['status']))

        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(title=channels[0]['channel']['display_name'], text='Game: '+channels[0]['game']+'\n觀看人數: '+str(channels[0]['viewers']), thumbnail_image_url= channels[0]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[0]['channel']['url']),
            ]),
            CarouselColumn(title=channels[1]['channel']['display_name'], text='Game: '+channels[1]['game']+'\n觀看人數: '+str(channels[1]['viewers']), thumbnail_image_url= channels[1]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[1]['channel']['url']),
            ]),
            CarouselColumn(title=channels[2]['channel']['display_name'], text='Game: '+channels[2]['game']+'\n觀看人數: '+str(channels[2]['viewers']), thumbnail_image_url= channels[2]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[2]['channel']['url']),
            ]),
            CarouselColumn(title=channels[3]['channel']['display_name'], text='Game: '+channels[3]['game']+'\n觀看人數: '+str(channels[3]['viewers']), thumbnail_image_url= channels[3]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[3]['channel']['url']),
            ]),
            CarouselColumn(title=channels[4]['channel']['display_name'], text='Game: '+channels[4]['game']+'\n觀看人數: '+str(channels[4]['viewers']), thumbnail_image_url= channels[4]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[4]['channel']['url']),
            ]),
            CarouselColumn(title=channels[5]['channel']['display_name'], text='Game: '+channels[5]['game']+'\n觀看人數: '+str(channels[5]['viewers']), thumbnail_image_url= channels[5]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[5]['channel']['url']),
            ]),
            CarouselColumn(title=channels[6]['channel']['display_name'], text='Game: '+channels[6]['game']+'\n觀看人數: '+str(channels[6]['viewers']), thumbnail_image_url= channels[6]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[6]['channel']['url']),
            ]),
            CarouselColumn(title=channels[7]['channel']['display_name'], text='Game: '+channels[7]['game']+'\n觀看人數: '+str(channels[7]['viewers']), thumbnail_image_url= channels[7]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[7]['channel']['url']),
            ]),
            CarouselColumn(title=channels[8]['channel']['display_name'], text='Game: '+channels[8]['game']+'\n觀看人數: '+str(channels[8]['viewers']), thumbnail_image_url= channels[8]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[8]['channel']['url']),
            ]),
            CarouselColumn(title=channels[9]['channel']['display_name'], text='Game: '+channels[9]['game']+'\n觀看人數: '+str(channels[9]['viewers']), thumbnail_image_url= channels[9]['preview']['large'],
            actions=[
                URITemplateAction(label='開始觀看', uri=channels[9]['channel']['url']),
            ]),

        ])
        template_message = TemplateSendMessage(
            alt_text='當下人氣直播', template=carousel_template)
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
    channels = client.streams.get_live_streams(limit=10)
    # for i in range(10):
    #     print(channels[i]['channel']['display_name'])
    #     print(channels[i]['game'])
    #     print(channels[i]['viewers'])
    #     print(channels[i]['channel']['logo'])
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
