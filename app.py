from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('n2/oMSzCaz1Jr+egWM+Ib4sSruyKp/0J/TxMYm/hIsljg7eQ8NAiq+1DT+cqYe7ucoIsQyGYT+Sqz7RsSIP8HT0VvXrcIyzYdh30evSqZbYnWDmzxSzlGsgo3gbtYN45Up6q/1RVIPu9sAvJfZ+6zgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('792dd29a8e0b85c5ca672936e3822d9a')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '請輸入早安/愛你/想你或是貼圖'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='6632',
            sticker_id='11825376'
        )
        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return
    
    if msg == '早安':
        r = '早安阿寶～祝你有美好的一天哦'
    elif msg in ['愛妳', '愛你', 'Love u', 'love you', 'love u']:
        r = '我也愛你哦 今天工作還好嗎'
    elif msg == '餓了':
        r = '我也餓了，你吃飯了嗎'
    elif msg in ['想你', '想妳']:
        r = '我也想你嘻嘻(羞)'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


    if '長輩圖' in msg:
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/uJUYDde.jpg',
            preview_image_url='https://i.imgur.com/uJUYDde.jpg'
        )
        line_bot_api.reply_message(
                event.reply_token,
                image_message)
        return


if __name__ == "__main__":
    app.run()