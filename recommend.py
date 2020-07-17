import pymysql
import re
import sql_acount

## 連接資料庫
host = sql_acount.login()[2]             # GCP Cloud SQL 的 IP
port = 3306                         # MySQL 的 Port
user = sql_acount.login()[0]        # 帳號存放在另外的位置
password = sql_acount.login()[1]    # 密碼存放在另外位置
db = "i_member"                     # 選擇在 MySQL 上你操作時要用的 DataBase
connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset="utf8")   # 搭起 GCP Cloud SQL(MySQL) 橋梁


## 檢查每日營養素差值表是否存在
def check_difference(m_id):
    try:
        # 主要執行的 SQL
        sql = f"""
        SELECT record_time, m_id FROM i_member.everyday_nutrients_difference WHERE m_id = "{m_id}" AND record_time = CURDATE();
        """
        cursor = connection.cursor()    # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子
        cursor.execute(sql)             # 執行 SQL 指令
        check = cursor.fetchone()[0]    # 判斷 "當天", "某會員" 有沒有資料
        return "exist"
    except TypeError:
        return "no exist"

## 新增一個拿來扣減用的差值表
def insert_difference(m_id):
    sql = f"""
    INSERT INTO i_member.everyday_nutrients_difference
        SELECT curdate(), m_id, m_group, nutrients, content FROM i_member.demand_schedule WHERE m_id = "{m_id}" ORDER BY ds_time DESC LIMIT 21;
    """
    cursor = connection.cursor()  # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子
    cursor.execute(sql)  # 執行 SQL 指令
    # connection.commit()  # commit 所有暫存的 SQL 指令
    connection.close()   # 關閉 SQL 的操作，此時 cursor 當中有暫存 SQL 指令會被清除
    print("difference_Data INSERT to MySQL successfully")

## 修改差值表
def update_difference(m_id):
    # 開啟 MySQL UPDATE 功能
    cursor = connection.cursor()  # 可以把這當作操作MySQL時，你的鍵盤滑鼠 / 或者暫時存放 SQL 指令的桶子

    # 開啟 MySQL UPDATE 權限
    sql_set0 = """
        SET SQL_SAFE_UPDATES = 0;
        """
    cursor.execute(sql_set0)    # 執行 SQL 指令

    # 暫時開啟 GROUP BY 權限
    sql_set_group = """
    SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
    """
    cursor.execute(sql_set_group)   # 執行 SQL 指令

    # 主要執行的 SQL
    sql_update = f"""
    UPDATE i_member.everyday_nutrients_difference 
    SET difference = (	
                        SELECT cccc1.difference 
                        FROM (
                                SELECT ccc2.nutrients, round((ccc2.content-ccc1.oneday_ingest), 2) AS "difference" 
                                FROM (
                                        SELECT cc1.new_date, cc1.m_id, cc3.nutrients, sum(cc2.per100_content * cc1.gram / 100) AS "oneday_ingest"
                                        FROM (
                                                SELECT c1.m_id, c1.eat_food, c2.R_id, c1.gram, SUBSTRING(c1.eat_time, 1, 8) AS "new_date"
                                                FROM i_member.everyday_user_eat c1
                                                JOIN i_nutrition.original_recipe c2
                                                ON c1.eat_food = c2.RecipeName
                                                WHERE c1.m_id = "{m_id}"
                                                GROUP BY c1.eat_food, c1.eat_time
                                                ) cc1
                                        JOIN i_nutrition.recipe_nutrients_content_per100g_normalization cc2
                                        ON cc1.R_id =  cc2.r_id
                                        JOIN i_nutrition.original_nutrients cc3
                                        ON cc2.n_id = cc3.n_id
                                        GROUP BY cc3.nutrients, cc1.new_date
                                        HAVING new_date = (SELECT CONCAT(YEAR(CURDATE()), "0", MONTH(CURDATE()), DAY(CURDATE())))
                                        ORDER BY cc2.n_id
                                        ) ccc1
                                JOIN (SELECT * FROM i_member.demand_schedule WHERE m_id = "{m_id}" ORDER BY ds_time DESC LIMIT 21) ccc2
                                ON ccc1.nutrients = ccc2.nutrients
                                ) cccc1             
                        WHERE i_member.everyday_nutrients_difference.nutrients = cccc1.nutrients LIMIT 1),
        record_time = CURDATE()
    WHERE m_id = "{m_id}" AND record_time = CURDATE();
    """

    cursor.execute(sql_update)

    # 關閉 MySQL UPDATE 功能
    sql_set1 = """
    SET SQL_SAFE_UPDATES = 1;
    """
    cursor.execute(sql_set1)  # 執行 SQL 指令

    # connection.commit()  # commit 所有暫存的 SQL 指令
    connection.close()  # 關閉 SQL 的操作，此時 cursor 當中有暫存 SQL 指令會被清除

    print("difference_Data UPDATE to MySQL successfully")

def do_difference(m_id):
    # m_id = "M10000001"
    check_result = check_difference(m_id)

    if check_result == "exist":         # 如果已經有資料要從 "差值表" 取資料對"當天"這時間點進行 UPDATE
        update_difference(m_id)         # 代入 m_id 修改已有的差值表


    elif check_result == "no exist":    # 如果沒有資料要從 "基準表" 當中取資料對"當天"這時間點進行 INSERT
        insert_difference(m_id)         # 代入 m_id 從基準表 TABLE 中取出最新某會員最新的基準表後 INSERT 進差值表 TABLE當中

    else:
        print("CHECK ERROR")


