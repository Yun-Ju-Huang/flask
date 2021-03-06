from flask import Flask, render_template,request,redirect,url_for,make_response,flash
import re, os
from flask_bootstrap import Bootstrap
import pymysql
import sql_acount
import to_sql
import kafkaProducer_newUser
import kafkaProducer_dailyEat
import recommend


# 起首式###############################################################################################################
app=Flask(__name__)
# app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1
bootstrap = Bootstrap(app)
## 連接資料庫
cursor = sql_acount.acount2()        # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子

######################################################################################################################





# 接資料用#############################################################################################################
## 登入後的會員Email
user_email = {}

## 儲存會員的問卷資料 {s1:(), s2:()}
survey_data = {}
######################################################################################################################





# HOME相關頁面#########################################################################################################
## 連接到HOME
@app.route('/')
def home():
    return render_template('home_try.html')     # 開啟home的HTML


## 連接到success.home頁面
@app.route('/success')
def success():
    user = user_email["email"]                              # 用上面字典接住的username
    return render_template('success.html', username=user)   # 開啟success的頁面，並輸出username


## 連接到推薦頁面
@app.route('/recommend')
def recommend():
    recommend = to_sql.select_5()
    return render_template('recommend.html', value=recommend, username=user_email["email"])


## 網頁：問卷填寫完畢的感謝頁面 / 會在畫面停留5秒後跳轉到指定頁面
@app.route("/survey/thanks", methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')


######################################################################################################################





# login_try 相關#######################################################################################################
## 連接到登入頁面
@app.route('/login_try',methods=['GET', 'POST'])                        # 只要有表格需輸入就須寫『,methods=['GET', 'POST']』
def login_try():
    if request.method == 'POST':
        email= request.form.get("aausername")                           # 在頁面中抓HTML是"aausername"的資訊
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$', email):        # 寫判斷式確認登入是否為Email格式
            check_email  = to_sql.check_survey_email(email)             # 呼叫to_sql的check_survey_email確認該email是否有在SQL中
            if check_email == "exist":
                user_email["email"] = request.form.get("aausername")    # 如果有就將username+入上方字典中以{["email"]:XXX@gmail.com}的格式
                return  redirect(url_for('success'))                    # 轉到success的函式中
            else:

                return "登入失敗!!!請確認帳號與密碼是否正確!!!" +\
                       render_template('login_try.html')                # 若Email沒有在SQL中會回傳此訊息+頁面


        else:
            return "請輸入正確信箱!!" + \
                   render_template('login_try.html')                    # 若Email格式錯誤會回傳此訊息+頁面
    return render_template('login_try.html')                            # 此為呼叫login_try()這函式就會回傳的頁面

### line專用###
## 登入頁面用於 "line+基本問卷"
@app.route('/login_try2',methods=['GET', 'POST'])                       # 只要有表格需輸入就須寫『,methods=['GET', 'POST']』
def login_try2():
    if request.method == 'POST':
        email= request.form.get("aausername")                           # 在頁面中抓HTML是"aausername"的資訊
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$', email):        # 寫判斷式確認登入是否為Email格式
            check_email  = to_sql.check_survey_email(email)             # 呼叫to_sql的check_survey_email確認該email是否有在SQL中
            if check_email == "exist":
                user_email["email"] = request.form.get("aausername")    # 如果有就將username+入上方字典中以{["email"]:XXX@gmail.com}的格式
                return  redirect(url_for('survey'))                     # 轉到survey的函式中
            else:

                return "登入失敗!!!請確認帳號與密碼是否正確!!!" + \
                       render_template('login_try2.html')               # 若Email沒有在SQL中會回傳此訊息+頁面

        else:
            return "請輸入正確信箱!!" + \
                   render_template('login_try2.html')                   # 若Email格式錯誤會回傳此訊息+頁面
    return render_template('login_try2.html')                           # 此為呼叫login_try2()這函式就會回傳的頁面


### line專用###
## 登入頁面用在"line+每日飲食問卷"
@app.route('/login_try3',methods=['GET', 'POST'])                        #只要有表格需輸入就須寫『,methods=['GET', 'POST']』
def login_try3():
    if request.method == 'POST':
        email= request.form.get("aausername")                            # 在頁面中抓HTML是"aausername"的資訊
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$', email):         # 寫判斷式確認登入是否為Email格式
            check_email  = to_sql.check_survey_email(email)              # 呼叫to_sql的check_survey_email確認該email是否有在SQL中
            if check_email == "exist":
                user_email["email"] = request.form.get("aausername")     # 如果有就將username+入上方字典中以{["email"]:XXX@gmail.com}的格式
                return  redirect(url_for('daily_record'))                # 轉到daily_record的函式中
            else:

                return "登入失敗!!!請確認帳號與密碼是否正確!!!" + \
                       render_template('login_try3.html')                # 若Email沒有在SQL中會回傳此訊息+頁面


        else:
            return "請輸入正確信箱!!" + \
                   render_template('login_try3.html')                    # 若Email格式錯誤會回傳此訊息+頁面
    return render_template('login_try3.html')                            # 此為呼叫login_try3()這函式就會回傳的頁面


## 連接到註冊會員頁面
@app.route('/create',methods=['GET', 'POST'])                                               #只要有表格需輸入就須寫『,methods=['GET', 'POST']』
def create():
    if request.method == 'POST':                                                            # 當網頁發生 POST method 則會獲取網頁中使用者填入的資料
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$', request.form.get("name")):         # 寫判斷式確認登入是否為Email格式
            check_email = to_sql.check_survey_email(request.form.get("name"))               # 呼叫to_sql的check_survey_email確認該email是否有在SQL中
            if check_email == "exist":
                return "信箱已被註冊!!" + \
                       render_template('create_new_account.html')                            # 若Email有在SQL中會回傳此訊息+頁面
            else:
                email = request.form.get("name")                                             # 若Email沒有在SQL中，用變數接住
                return "您好!!" + request.form.get("name") + \
                       "註冊成功，請稍待片刻~~~系統將會於3秒後自動跳轉回首頁..." + \
                       '<meta http-equiv="refresh" content="3;url=/">', \
                       outside_new_account(email)                                            # 回傳訊息+呼叫outside_new_account(email)這函式將變數放入，在SQL中心增資料
        else:
            return "請輸入正確信箱!!" + render_template('create_new_account.html')            # 若Email格式錯誤會回傳此訊息+頁面
    return render_template('create_new_account.html')                                        # 此為呼叫create()這函式就會回傳的頁面

def outside_new_account(email):
    print(email)
    to_sql.insersql_new_account(email)
    to_sql.SQLcommit("insert")\


## 連接到忘記密碼頁面
@app.route('/click',methods=['GET', 'POST'])                                                     #只要有表格需輸入就須寫『,methods=['GET', 'POST']』
def click():
    if request.method == 'POST':                                                                 # 當網頁發生 POST method 則會獲取網頁中使用者填入的資料
        if re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$',  request.form.get("nname")):            # 寫判斷式確認登入是否為Email格式
            return "您好!!" + request.form.get("nname")+\
                   "，已寄送相關文件至您的信箱!!請稍待片刻~~~系統將會於3秒後自動跳轉回首頁..."+\
                   '<meta http-equiv="refresh" content="3;url=/">'                               # 在頁面中抓HTML是"nname"的資訊
        else:
            return "請輸入正確信箱!!" + render_template('click.html')                             # 若Email格式錯誤會回傳此訊息+頁面
    return render_template('click.html')                                                         # 此為呼叫create()這函式就會回傳的頁面
######################################################################################################################






#問卷資料##############################################################################################################
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
        return render_template('thanks.html'), outside_daily(daily_list)   # 進入到指定頁面，同時將資料往 MySQL 中送出
    return render_template('daily_record.html')


def outside():
    # 判斷暫存在 survey_data 中資料的狀況，排除各種可能空值情形
    if (survey_data["s1"] != "" and survey_data["s1"] != () and survey_data["s1"] != None) and \
            (survey_data["s2"] != "" and survey_data["s2"] != () and survey_data["s2"] != None):
        print(survey_data)

        m_id = to_sql.search_mid(user_email["email"])  # 導入 自訂套件 to_sql 獲取該 email 使用者在 SQL上 的 m_id (PK)

        check_result = to_sql.check_survey_mid(m_id)    # 導入 自訂套件 to_sql 查看"當日"的 m_id 是否存在於表格 member 當中
        if check_result == "exist":
            to_sql.updatesql_survey(m_id, survey_data["s1"])    # 導入 自訂套件 to_sql 傳入問卷一的資料 UPDATE
            to_sql.updatesql_survey2(m_id, survey_data["s2"])   # 導入 自訂套件 to_sql 傳入問卷二的資料 UPDATE
            to_sql.SQLcommit("update")    # commit 在自訂套件 to_sql 中下的所有 SQL UPDATE 指令
            kafkaProducer_newUser.to_kafka(m_id, survey_data["s1"])  # 導入自訂套件 kafkaProducer_newUser 傳入問卷一資料進 kafka

        elif check_result == "no exist":
            to_sql.insertsql_survey(m_id, survey_data["s1"])    # 導入 自訂套件 to_sql 傳入問卷一的資料 INSERT
            to_sql.insertsql_survey2(m_id, survey_data["s2"])   # 導入 自訂套件 to_sql 傳入問卷二的資料 INSERT
            to_sql.SQLcommit("insert")    # commit 在自訂套件 to_sql 中下的所有 SQL INSERT 指令
            kafkaProducer_newUser.to_kafka(m_id, survey_data["s1"])  # 導入自訂套件 kafkaProducer_newUser 傳入問卷一資料進 kafka

        else:
            print("OUTSIDE ERROR")
            pass


def outside_daily(daily_data):
    print(daily_data)
    m_id = to_sql.search_mid(user_email["email"])  # 導入 自訂套件 to_sql 獲取該 email 使用者在 SQL上 的 m_id (PK)
    to_sql.insertsql_dailyrecord(m_id, daily_data)  # 導入 自訂套件 to_sql 傳入每日飲食紀錄表的資料
    to_sql.SQLcommit("insert")    # commit 在自訂套件 to_sql 中下的所有 SQL INSERT 指令
    recommend.do_difference(m_id)  # 導入自訂套件 recommend 產生新的差值表
    kafkaProducer_dailyEat.to_kafka(m_id)  # 導入自訂套件 kafkaProducer_dailyEat 傳入每日飲食紀錄表的資料進 kafka
######################################################################################################################





#Kibana相關############################################################################################################
## 連接到kibana(天)
@app.route('/kibana/day')
def kibana_day():
     return render_template('kibana_day.html')


## 連接到kibana(周)
@app.route('/kibana/week')
def kibana_week():
    return render_template('kibana_week.html')
######################################################################################################################






if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,port=port,host="0.0.0.0")
    # app.run(debug=True)