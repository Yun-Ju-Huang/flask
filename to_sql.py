import pymysql
import re
import sql_acount

## 連接資料庫
host = "35.229.172.113"             # GCP Cloud SQL 的 IP
port = 3306                         # MySQL 的 Port
user = sql_acount.login()[0]        # 帳號存放在另外的位置
password = sql_acount.login()[1]    # 密碼存放在另外位置
db = "i_member"                     # 選擇在 MySQL 上你操作時要用的 DataBase
connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset="utf8")   # 搭起 GCP Cloud SQL(MySQL) 橋梁



def search_mid(email):
    sql = """
    SELECT m_id FROM i_member.myuser WHERE email = "{}";
    """.format(email)   # 透過 email 找到 m_id (PRIMARY KEY)
    cursor = connection.cursor()    # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子
    cursor.execute(sql)             # 執行 SQL 指令，此時指令還處在暫存狀態，因為尚未 commit
    m_id = cursor.fetchone()[0]     # 執行 SQL 指令，從 SQL 獲取 m_id
    return m_id

def insertsql_survey(m_id, data):
    m_id = m_id             # 使用者的 m_id (PRIMARY KEY)
    m_name = data[0]        # 使用者的 姓名
    m_sex = data[1]         # 使用者 性別
    m_birthday = data[2]    # 使用者 生日日期
    m_height = data[3]      # 使用者 身高
    m_weight = data[4]      # 使用者 體重
    m_target = data[5]      # 使用者 飲食目標
    cursor = connection.cursor()  # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子

    sql = """
    INSERT INTO i_member.member
    (m_id, m_name, m_sex, m_birthday, m_height, m_weight, m_target)
    VALUES
    ("{}", "{}", {}, {}, {}, {}, "{}");
    """.format(m_id, m_name, m_sex, m_birthday, m_height, m_weight, m_target)     # 建立指令：將上述信息 INSERT 進表格

    cursor.execute(sql)             # 執行 SQL 指令，此時 INSERT 指令還處在暫存狀態，因為尚未 commit
    print("member load successfully")



def insertsql_survey2(m_id, data):
    m_id = m_id             # 使用者的 m_id (PRIMARY KEY)
    da_id = data[0]         # 使用者 平常活動狀況
    ds_id = data[1]         # 使用者 平常運動類型
    sf_id = data[2]         # 使用者 運動頻率
    ec_id = data[3]         # 使用者 飲食狀況
    eof_id = data[4]        # 使用者 外食頻率
    ne_id_list = data[5]    # 使用者 飲食過敏 (多項)
    sc_id = data[6]         # 使用者 睡眠狀況
    mc_id = data[7]         # 使用者 精神狀況
    dc_id  = data[8]        # 使用者 排便狀況
    cursor = connection.cursor()  # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子

    sql2 ="""
    INSERT INTO i_member.member_state 
    (m_id, da_id, ds_id, sf_id, ec_id, eof_id, sc_id, mc_id, dc_id)
    VALUES 
    ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");    
    """.format(m_id, da_id, ds_id, sf_id, ec_id, eof_id, sc_id, mc_id, dc_id)   # 建立指令：將上述信息 INSERT 進表格

    cursor.execute(sql2)    # 執行 SQL 指令，此時 INSERT 指令還處在暫存狀態，因為尚未 commit
    print("member_state load successfully")

    for ne_id in ne_id_list:    # 透過迴圈逐一取出飲食過敏項目
        sql2_ne ="""
        INSERT INTO member_state_not_eat 
        (m_id, ne_id)
        VALUES 
        ("{}", "{}");
        """.format(m_id, ne_id)     # 建立指令：將飲食過敏信息逐一 INSERT 進表格

        cursor.execute(sql2_ne)     # 執行上述所有 SQL 指令，此時指令還處在暫存狀態，因為尚未 commit
    print("member_state_not_eat load successfully")


def insertsql_dailyrecord(m_id, daily_data):
    food_list = daily_data[0]   # 使用者當日吃的所有食物 (多項)
    gram_list = daily_data[1]   # 使用者當日吃的所有食物各自的公克重 (多項)
    time_list = daily_data[2]   # 使用者當日吃的所有食物各自的時間點 (多項)
    water = daily_data[3]   # 使用者 今日飲水量
    cursor = connection.cursor()    # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子

    for food, gram, time in zip(food_list, gram_list, time_list):   # 透過迴圈逐一取出使用者當日飲食狀況
        sql = """
        INSERT INTO everyday_user_eat 
        (m_id, eat_food, gram, eat_time)
        VALUES 
        ("{}", "{}", {}, "{}");    
        """.format(m_id, food, gram, time)  # 建立指令：將取出的信息逐一 INSERT 進表格

        cursor.execute(sql)  # 執行上述所有 SQL 指令，此時 INSERT 指令還處在暫存狀態，因為尚未 commit
    print("everyday_user_eat load successfully")

    sql2 = """
    INSERT INTO everyday_user_drink 
    (m_id, drink, drink_time)
    VALUES 
    ("{}", {}, "{}");
    """.format(m_id, water, time_list[-1])  # 建立指令：將取出的信息逐一 INSERT 進表格 / 時間部分取自最後一餐登陸的時間

    cursor.execute(sql2)    # 執行 SQL 指令，此時 INSERT 指令還處在暫存狀態，因為尚未 commit
    print("everyday_user_drink load successfully")

def SQLcommit():
    print("Starting insert data to MySQL")
    cursor = connection.cursor()    # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子
    connection.commit() # commit 所有暫存的 SQL 指令
    cursor.close()  # 關閉 SQL 的操作，此時 cursor 當中有暫存 SQL 指令會被清除
    print("Data insert to MySQL successfully")

















