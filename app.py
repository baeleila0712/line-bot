from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
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
    r = '請輸入早安/你好/愛你/想你/情侶間常用的關鍵字哦'

    if msg == '早安':
        r = '早安阿寶～祝你有美好的一天哦'

    elif msg == '餓了':
        r = '我也餓了，你吃飯了嗎'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()