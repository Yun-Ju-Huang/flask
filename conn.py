from flask import Flask, request, abort, render_template, flash, redirect, url_for
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import requests, re, json, pymysql
from lable import sendQuiclreply1, sendQuiclreply, sendQuiclreply3
from lable1 import ButtonsTemplate_send_message
from inputmysql import putintomysql, checkmysql, user_con_household_key, show_user_info
# from getuser import loginline, send_message,


line_bot_api = LineBotApi("x3/1rgo+dlEzHwgPKk72OKBZV2LAGAqBXiu8yXLlmuz5v0K/qnA4FS2Or1rR26Jtfz71JlR2HRujSycHxmUqABkqkkU9CjEilhbBGvr56JJQ9ekdWSWDCwTf6/+x5Jn2pkw4heWFE4tRDVWJ74FzYAdB04t89/1O/w1cDnyilFU=")  # 在 line_developer取得)
handler = WebhookHandler('9122ed5a8fae4f9ed8619df980757d74')


app = Flask(__name__)
user_id = ''
display_name = ''
checkuserid = ''
msg = ''

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

@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/home/loginurl/sucess/<username>', methods=['GET', 'POST'])
def success(username):
    return render_template('sucess.html', username=username)

@app.route('/aaa')
def aaa():
    return render_template('test.html')


#歷史資料
@app.route('/aabbcc')
def example(checkuserid):
    # checkuserid = 9028
    conn = pymysql.connect(host="1.tcp.ap.ngrok.io", user="16", passwd="eb101_smart", db="PStage", port=20534, charset='utf8', use_unicode=True)
    cursor = conn.cursor()
    cursor.execute("SELECT date_time, product_chnm, quantity, product_price FROM PStage.transaction_data_Det where transaction_data_Det.household_key in (SELECT line_smart.household_key FROM PStage.line_smart WHERE line_smart.user_id = '{}');".format(checkuserid))
    data = cursor.fetchall()
    print(data)
    print(type(data))
    return render_template("login123.html", value=data)



#登入
@app.route('/home/loginurl', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(checkuserid, username, password)
        try:
            if login_check(checkuserid, username, password):
                flash('Login Success!')
                global status
                msg = 'True'
                return redirect(url_for('success', username=request.form.get('username')))
        except:
            if login_check(checkuserid, username, password):
                flash('Login Success!')
                return redirect(url_for('success', username=request.form.get('username')))
        else:
            print(checkuserid, username, password)
            flash('<h1>登入失敗<h1>')
            return '<center>查無帳號，將導到註冊頁面....' \
                   '    <br>' \
                   '<meta http-equiv="refresh" content="5;url=https://caf7c747.ngrok.io/home/signon" />'\
                   '</center>'
    return render_template('login.html')

def login_check(checkuserid, username, password):
    """登入帳號密碼檢核"""
    # result
    a = checkmysql()
    if (checkuserid, username, password) in a:
        print(checkuserid)
        print("登入成功")
        return True

    else:
        print("登入失敗")
        return False
#註冊帳號密碼
@app.route('/home/signon', methods=['GET', 'POST'])
def getnewmember():
    if request.method == 'POST':
        newname = request.form.get('newusername')
        newpassword = request.form.get('newpassword')
        print(checkuserid, display_name, newname, newpassword)
        try:
            if putintomysql(checkuserid,  display_name, newname, newpassword):
                print(user_id, display_name, newname, newpassword)
                print('done')
                flash('<h1>註冊成功 ， 請使用帳號進行登入～<h1>')
            return redirect(url_for('hello', username=request.form.get('newusername')))
        except:
            return '<h1>註冊失敗 ， 請重新註冊一次或取消註冊～<h1>' \
                   '<meta http-equiv="refresh" content="5;url=https://caf7c747.ngrok.io/home/signon" />'
    return render_template('registrate.html')


@app.route('/hello/<username>', methods=['GET', 'POST'])
def hello(username):
    return render_template('hello.html', username=username)



reply_message_list = [
    TextSendMessage(text="關注區塊鏈技術，掌握市場脈動。"),
    TextSendMessage(text="人類所以充滿驚奇，在於人體那一精密又不可探究的系統。佈滿神經元的大腦，而後延展遍歷人體。\\n\\n區塊鏈就好比是人體那驚奇的神經系統，社會是我們的人身，在全身佈滿了神經後，造就了不可思量的奧妙生命。\\n\\n點選菜單，了解區塊鏈前世今生，以文字輸入 more，得到更多資訊。)")]


#line-bot code
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):

    # 取出消息內User的資料
    profile = line_bot_api.get_profile(event.source.user_id)
    print(profile)

    profile_dic = vars(profile)
    displayname = profile_dic.get('display_name')
    userid = profile_dic.get('user_id')
    global user_id, display_name
    user_id = userid
    display_name = displayname

    line_bot_api.reply_message(event.reply_token, reply_message_list)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    profile_dic = vars(profile)

    # msg = msg.encode('utf-8')
    global checkuserid, display_name
    display_name = profile_dic.get('display_name')
    userId = event.source.user_id
    checkuserid = userId

    # profile_data = {'Authorization': 'Bearer ' + 'CCbJVrY/up5EDoUVqFVbF/ULKruHAypgZVWmlH4RZYxm6yrzL4f+R2wEj2+M3F9/1FD2S4EMEZryUpjy+hyJxA5a5+6rIr1mBc76DdyW3hzJxGkfOMQHqP33iobNUUbnt3LNYmjnWUph3rxcNs92AgdB04t89/1O/w1cDnyilFU='}
    # profile = requests.get('https://api.line.me/v2/bot/profile/' + userId, headers=profile_data)

    print(checkuserid, display_name)

    if re.match('你好', msg) or re.match('hi', msg):
        line_bot_api.reply_message(event.reply_token, reply_message_list)
    elif msg in ('查詢付費', '流程', '結帳', '註冊', '查詢'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請點選選點'關於APP'"))
    elif msg == "熱門商品":
        example(checkuserid)
    elif msg == "Smart活動":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="目前活動還在準備中...請耐心等待唷！"))
    elif msg == "會員專區":
        ButtonsTemplate_send_message(event)
    elif msg == "歷史紀錄":
        sendQuiclreply3(event)
    elif msg == '我要登入':
            result = show_user_info(checkuserid)
            print(result)
            if result == None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=("找不到會員，請再試一次!")))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='登入成功,您的帳號是 {}, 密碼是 {}，請輸入 開始使用'.format(result[0],result[1])))
            result = show_user_info(checkuserid)

    else:
        pass
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(
            # text=("您已是會員，使用Line登入，您的帳號是 {}, 密碼是 {}").format(result[0], result[1])))

        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='系統還在準備中...'))
        # line_bot_api.broadcast(TextSendMessage(text='抱歉我在測試!'))
        # line_bot_api.push_message(userId, TextSendMessage(text='歡迎會員！!'))



if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'sharon'
    app.run()
