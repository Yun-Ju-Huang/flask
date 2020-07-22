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


## 檢查當日營養素差值表是否存在
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

## 新增一個當日拿來扣減用的差值表
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

## 修改當日差值表
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
    SET difference =(
                        SELECT ccc1.difference
                        FROM (
                                SELECT cc1.record_time, cc1.m_id, cc2.m_group, cc1.nutrients, cc2.content, cc1.total_daily_content, (cc2.content-cc1.total_daily_content) AS "difference"
                                FROM (
                                        SELECT c1.record_time, c1.m_id, c1.n_id, c2.nutrients, sum(c1.daily_content) AS "total_daily_content"
                                        FROM for_foodgroup.daily_nutrients c1
                                        JOIN i_nutrition.original_nutrients c2
                                        ON c1.n_id = c2.n_id
                                        GROUP BY c1.n_id, c1.m_id, c1.record_time 
                                        ORDER BY c1.n_id
                                        ) cc1
                                JOIN (
                                        SELECT * 
                                        FROM i_member.demand_schedule 
                                        WHERE m_id = "{m_id}" 
                                        ORDER BY ds_time DESC 
                                        LIMIT 21
                                        ) cc2
                                ON cc1.m_id = cc2.m_id AND cc1.nutrients = cc2.nutrients) ccc1
                        WHERE i_member.everyday_nutrients_difference.nutrients = ccc1.nutrients LIMIT 1),
        record_time = CURDATE()
    WHERE m_id = "{m_id}" AND record_time = CURDATE();
    """
    cursor.execute(sql_update)
    connection.commit()  # commit 所有暫存的 SQL 指令

    # 關閉 MySQL UPDATE 功能
    sql_set1 = """
    SET SQL_SAFE_UPDATES = 1;
    """
    cursor.execute(sql_set1)  # 執行 SQL 指令


    connection.close()  # 關閉 SQL 的操作，此時 cursor 當中有暫存 SQL 指令會被清除

    print("difference_Data UPDATE to MySQL successfully")

def do_difference(m_id):

    check_result = check_difference(m_id)

    if check_result == "exist":         # 如果已經有資料要從 "差值表" 取資料對"當天"這時間點進行 UPDATE
        update_difference(m_id)         # 代入 m_id 修改已有的差值表


    elif check_result == "no exist":    # 如果沒有資料要從 "基準表" 當中取資料對"當天"這時間點進行 INSERT
        insert_difference(m_id)         # 代入 m_id 從基準表 TABLE 中取出最新某會員最新的基準表後 INSERT 進差值表 TABLE當中

    else:
        print("CHECK ERROR")


# m_id = "M10000004"
# do_difference(m_id)