from flask import Flask, render_template,request,redirect,url_for
import re, os
app=Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1
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

## 輸出到sql用的函式
def outside(what, *args):
    if what == "survey":
        data = [*args]
    elif what == "survey2":
        data = [*args]
    elif what == "daily_record":
        data = [*args]
        # print(data)
    # to_sql.insertsql(member)  # 連接 sql insert 資料



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,port=port)

