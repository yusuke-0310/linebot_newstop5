import os

import pya3rt

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

import requests

from bs4 import BeautifulSoup

app = Flask(__name__)

line_bot_api = LineBotApi('ShoGcY9IRr/1yY3APXaXwUqdoZ5+r7xq2zYATtt+I80G0/7q9oJ+xCO3EuwCKCv0ak/UTZtjEgFLqIC3SoytmLiXVBxu/J64ljb4oG6Wet848qw8+0HNiY9Lq30OJgv976MYDXwe4nT3DcoYthHqMgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6c55ce68706f9966ed31ddbd838cce55')

#@app.route以降は('〇〇')の部分に指定したURL末尾を記載することで、URLによってその後のコードが実行される
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
    reply = create_reply(event.message.text)
    news = newstop5(event.message.text)
    #event.message.textにLINEで送ったメッセージが入る
    messages = []
    for i in news:
        messages.append(TextSendMessage(text=i))
        print(news)
    line_bot_api.reply_message(event.reply_token, messages)
    #replyにcreate_replyの内容が反映される。replyに仮にevent.message.textを入れると送った内容がそのまま返信される

def create_reply(user_text):
    apikey = 'DZZPKSBU5XUE5wY9tfXf4QCEuOdg36C1'
    client = pya3rt.TalkClient(apikey)
    res = client.talk(user_text)

    return res['results'][0]['reply']

def newstop5(user_text):
    url = 'https://news.yahoo.co.jp/flash?p=1'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    response = response.text
    bs = BeautifulSoup(response, 'html.parser')
    div_flashSummary_primary = bs.select('div.flashSummary_primary')
    result = []
    false = ['ニュースと入力してください。']
    count = 0
    if user_text == 'ニュース':
        while True:
            for div_title in div_flashSummary_primary[count].select('p.flashSummary_title'):
                newstext = div_title.text
                #result.append(newstext)
                #print(div_title.text)
            for div_title_link in div_flashSummary_primary[count].find_all('a'):
                div_title_link = div_title_link.get('href')
                newslink = div_title_link
                result.append(newslink)
                #print(div_title_link)

                #return newstext
                #continue
                #return newslink
                #continue
                count += 1
                #return newstext, newslink
                #continue
            if count >= 5:
                return result
                #return '成功'
                break

                #return newstext, newslink
    else:
        return false
        return 'ニュースと入力してください。'
    
    print('検索したいキーワードを入力してください。')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    app.run()

    #app.run()
