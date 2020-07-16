from flask import Flask, render_template,request,redirect,url_for
import re, os
from flask_bootstrap import Bootstrap
import pymysql
import sql_acount
import to_sql

app=Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1
bootstrap = Bootstrap(app)

## 連接資料庫
host = "35.229.172.113"             # GCP Cloud SQL 的 IP
port = 3306                         # MySQL 的 Port
user = sql_acount.login()[0]        # 帳號存放在另外的位置
password = sql_acount.login()[1]    # 密碼存放在另外位置
db = "i_member"                     # 選擇在 MySQL 上你操作時要用的 DataBase
connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset="utf8")   # 搭起 GCP Cloud SQL(MySQL) 橋梁
cursor = connection.cursor()        # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子

@app.route('/login',methods=['GET', 'POST'])
##連接到登入頁面
def login_try():
    if request.method == 'POST':
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$',request.form.get("aausername")):
            return "您好!!" +request.form.get("aausername")+"請稍待片刻~~~系統將會於3秒後自動跳轉回首頁..."+'<meta http-equiv="refresh" content="3;url=http://127.0.0.1:5000/">'
        else:
            return "請輸入正確信箱!!" +render_template('login_try.html')


    return render_template('login_try.html')



##連接到註冊會員頁面
@app.route('/create',methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$', request.form.get("name")):
            return "您好!!" + request.form.get("name") + "註冊成功，請稍待片刻~~~系統將會於3秒後自動跳轉回首頁..."+'<meta http-equiv="refresh" content="3;url=http://127.0.0.1:5000/">'
        else:
            return "請輸入正確信箱!!" + render_template('create_new_account.html')

    return render_template('create_new_account.html')
##連接到忘記密碼頁面
@app.route('/click',methods=['GET', 'POST'])
def click():
    if request.method == 'POST':
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$',  request.form.get("nname")):
            return "您好!!" + request.form.get("nname")+"，已寄送相關文件至您的信箱!!請稍待片刻~~~系統將會於3秒後自動跳轉回首頁..."+'<meta http-equiv="refresh" content="3;url=http://127.0.0.1:5000/">'
        else:
            return "請輸入正確信箱!!" + render_template('click.html')

    return render_template('click.html')
##連接到推薦頁面
@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

##連接到HOME
@app.route('/')
def home():
    return render_template('home_try.html')
##連接到每日飲食紀錄
@app.route("/daily_record", methods=['GET', 'POST'])
def daily_record():
    if request.method == 'POST':
        food_list = []
        gram_list = []
        time_list = []
        for num in range(11):
            if num == 0:
                food = request.form.get("food")
                gram = request.form.get("gram")
                time = request.form.get("time")
                if (food and gram and time) != None and (food and gram and time) != "":
                    food_list.append(food)
                    gram_list.append(gram)
                    time_list.append(time)

            if num >= 1:
                food = request.form.get("food"+str(num))
                gram = request.form.get("gram" + str(num))
                time = request.form.get("time" + str(num))
                if (food and gram and time) != None and (food and gram and time) != "":
                    food_list.append(food)
                    gram_list.append(gram)
                    time_list.append(time)
        # outside("daily_record", food_list, gram_list, time_list)
        print(food_list, gram_list, time_list)
        return "填寫完成"   # 本日攝取頁面
    return render_template('daily_record.html')


@app.route("/survey", methods=['GET', 'POST'])
def survey():
    if request.method == "POST":
        user = request.form.get("user")
        sex = request.form.get("sex")
        age = request.form.get("age")
        height = request.form.get("height")
        weight = request.form.get("weight")
        target = request.form.get("target")
        outside("survey", user, sex, age, height, weight, target)
        return redirect(url_for("survey2"))
    return render_template("survey.html")

@app.route("/survey2", methods=['GET', 'POST'])
def survey2():
    if request.method == "POST":
        daily_activity = request.form.get("daily_activity")
        daily_sport = request.form.get("daily_sport")
        sport_freq = request.form.get("sport_freq")
        eat_condition = request.form.get("eat_condition")
        eatingout_freq = request.form.get("eatingout_freq")

        not_eat_list = []
        for num in range(1,7):
            ne_item = "not_eat0{}".format(num)
            if request.form.get(ne_item) != None:
                not_eat_list.append(request.form.get(ne_item))

        sleep_condition = request.form.get("sleep_condition")
        mental_condition = request.form.get("mental_condition")
        defecation_condition = request.form.get("defecation_condition")
        outside("survey2", daily_activity, daily_sport, sport_freq, eat_condition, eatingout_freq, not_eat_list, sleep_condition, mental_condition,
                defecation_condition)
        return render_template('thanks.html')

    return render_template('survey2.html')

@app.route("/survey/thanks", methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')

## 儲存會員的問卷資料 {s1:(), s2:()}
survey_data = {}


@app.route("/", methods=["GET", "POST"])
def price():
    title = "price123"
    return render_template("index.html", title=title)

# @app.route("/test")
# def test():
#     return render_template('test.html')

## 網頁：問卷一
@app.route("/survey", methods=['GET', 'POST'])
def survey():
    cursor.close()  # 進入網站時先關閉SQL的操作，此時 cursor 當中有暫存 SQL 指令會被清除
    if request.method == "POST":    # 當網頁發生 POST method 則會獲取網頁中使用者填入的資料
        user = request.form.get("user")          # 獲取，使用者 姓名
        sex = request.form.get("sex")            # 獲取，使用者 性別
        birthday = request.form.get("birthday")  # 獲取，使用者 生日日期
        height = request.form.get("height")      # 獲取，使用者 身高
        weight = request.form.get("weight")      # 獲取，使用者 體重
        target = request.form.get("target")      # 獲取，使用者 飲食目標

        survey_data["s1"] = (user, sex, birthday, height, weight, target)   # 將資料暫存在 survey_data

        return redirect(url_for("survey2"))     # 進入到問卷二頁面
    return render_template("survey.html")


## 網頁：問卷二
@app.route("/survey2", methods=['GET', 'POST'])
def survey2():
    cursor.close()  # 進入網站時先關閉 SQL 的操作，此時 cursor 當中有暫存 SQL 指令會被清除
    if request.method == "POST":    # 當網頁發生 POST method 則會獲取網頁中使用者填入的資料
        daily_activity = request.form.get("daily_activity")     # 獲取，使用者 平常活動狀況
        daily_sport = request.form.get("daily_sport")           # 獲取，使用者 平常運動類型
        sport_freq = request.form.get("sport_freq")             # 獲取，使用者 運動頻率
        eat_condition = request.form.get("eat_condition")       # 獲取，使用者 飲食狀況
        eatingout_freq = request.form.get("eatingout_freq")     # 獲取，使用者 外食頻率

        not_eat_list = []   # 獲取，使用者 飲食過敏 / 暫存使用者飲食過敏的全部品項
        for num in range(1,7):  # 過敏品項可能不只一種，透過迴圈取出
            ne_item = "not_eat0{}".format(num)
            if request.form.get(ne_item) != None:   # 排除位勾選的過敏項目
                not_eat_list.append(request.form.get(ne_item))

        sleep_condition = request.form.get("sleep_condition")           # 獲取 使用者 睡眠狀況
        mental_condition = request.form.get("mental_condition")         # 獲取 使用者 精神狀況
        defecation_condition = request.form.get("defecation_condition") # 獲取 使用者 排便狀況

        survey_data["s2"] = (daily_activity, daily_sport, sport_freq, eat_condition, eatingout_freq, not_eat_list,
                             sleep_condition, mental_condition, defecation_condition)   # 將資料暫存在 survey_data

        return render_template('thanks.html'), outside()    # 進入到感謝頁面，同時將資料往 MySQL 中送出

    return render_template('survey2.html')

## 網頁：問卷填寫完畢的感謝頁面 / 會在畫面停留5秒後跳轉到指定頁面
@app.route("/survey/thanks", methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')


# 網頁：每日飲食紀錄表
@app.route("/daily_record", methods=['GET', 'POST'])
def daily_record():
    cursor.close()  # 進入網站時先關閉 SQL 的操作，此時 cursor 當中有暫存 SQL 指令會被清除
    if request.method == 'POST':    # 當網頁發生 POST method 則會獲取網頁中使用者填入的資料
        food_list = []      # 暫存使用者當日吃的所有食物
        gram_list = []      # 暫存使用者當日吃的所有食物各自的公克重
        time_list = []      # 暫存使用者當日吃的所有食物各自的時間點
        drink_water = request.form.get("drink_water")   # 獲取 使用者 今日飲水量
        for num in range(11):   # 使用者當天可能不只吃一餐，透過迴圈逐一取出放入暫存
            if num == 0:
                food = request.form.get("food")     # 獲取 使用者 吃的食物
                gram = request.form.get("gram")     # 獲取 使用者 吃的食物的公克重
                time = request.form.get("time")     # 獲取 使用者 吃食物的時間點
                time2 = "".join(re.findall(r"[0-9]+", time))+"00"   # 將時間轉換成 INSERT SQL 時的形式

                # 排除空值輸入的狀況後，再放入暫存
                if (food and gram and time) != None and (food and gram and time) != "":
                    food_list.append(food)
                    gram_list.append(gram)
                    time_list.append(time2)
            if num >= 1:    # 從第二筆資料開始 html 中寫的 name 變數名稱會改變 ex, food > food 1
                food = request.form.get("food"+str(num))
                gram = request.form.get("gram" + str(num))
                time = request.form.get("time")
                time2 = "".join(re.findall(r"[0-9]+", time))+"00"

                if (food and gram and time) != None and (food and gram and time) != "":
                    food_list.append(food)
                    gram_list.append(gram)
                    time_list.append(time2)

        daily_list = (food_list, gram_list, time_list, drink_water)
        return "填寫完成", outside_daily(daily_list)   # 進入到指定頁面，同時將資料往 MySQL 中送出
    return render_template('daily_record.html')


def outside():
    # 判斷暫存在 survey_data 中資料的狀況，排除各種可能空值情形
    if (survey_data["s1"] != "" and survey_data["s1"] != () and survey_data["s1"] != None) and \
            (survey_data["s2"] != "" and survey_data["s2"] != () and survey_data["s2"] != None):
        print(survey_data)
        m_id = to_sql.search_mid("liao0707@gmail.com")  # 導入 自訂套件 to_sql 獲取該 email 使用者在 SQL上 的 m_id (PK)
        to_sql.insertsql_survey(m_id, survey_data["s1"])    # 導入 自訂套件 to_sql 傳入問卷一的資料
        to_sql.insertsql_survey2(m_id, survey_data["s2"])   # 導入 自訂套件 to_sql 傳入問卷二的資料
        to_sql.SQLcommit()    # commit 在自訂套件 to_sql 中下的所有 SQL INSERT 指令


def outside_daily(daily_data):
    print(daily_data)
    m_id = to_sql.search_mid("liao0707@gmail.com")  # 導入 自訂套件 to_sql 獲取該 email 使用者在 SQL上 的 m_id (PK)
    to_sql.insertsql_dailyrecord(m_id, daily_data)  # 導入 自訂套件 to_sql 傳入每日飲食紀錄表的資料
    to_sql.SQLcommit()    # commit 在自訂套件 to_sql 中下的所有 SQL INSERT 指令




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,port=port)

