import pymysql
import re
import sql_acount
import pandas as pd

# 連接資料庫
host = sql_acount.login()[2]              # GCP Cloud SQL 的 IP
port = 3306                         # MySQL 的 Port
user = sql_acount.login()[0]        # 帳號存放在另外的位置
password = sql_acount.login()[1]    # 密碼存放在另外位置
db = "i_nutrition"                     # 選擇在 MySQL 上你操作時要用的 DataBase
connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset="utf8")   # 搭起 GCP Cloud SQL(MySQL) 橋梁

## 找出某會員當日吃的東西
# def get_eat(m_id):
#     cursor = connection.cursor()
#     sql_set = """
#     SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
#     """
#     cursor.execute(sql_set)
#
#     sql = f"""
#     SELECT cc1.*
#     FROM (
#             SELECT c1.m_id, c1.eat_food, c1.gram, SUBSTRING(c1.eat_time, 1, 8) AS "new_date"
#             FROM for_foodgroup.everyday_user_eat_origin c1
#             WHERE c1.m_id = "{m_id}"
#             GROUP BY c1.eat_food, c1.eat_time
#             ) cc1
#     WHERE new_date = (SELECT CONCAT(YEAR(CURDATE()), SUBSTRING(CURDATE(), 6, 2), SUBSTRING(CURDATE(), 9, 2)));
#     """
#
#
#     cursor.execute(sql)
#     eat_list = cursor.fetchall()
#     return eat_list

## 依其所使用的公克數，得到吃的東西的24種營養素 (食材版)
def check_food(food_name, gram):
    cursor = connection.cursor()

    sql = f"""
    SELECT cc3.n_id, cc3.content * {gram} / 100 AS "content"
    FROM (
            SELECT *
            FROM (
                SELECT * 
                FROM i_nutrition.original_self_pronoun
                WHERE pronoun LIKE "%{food_name}%" 
                LIMIT 1
                ) c1 
            ) cc1
    JOIN i_nutrition.f_sp cc2
    ON cc1.sp_id = cc2.sp_id
    JOIN i_nutrition.f_n cc3
    ON cc2.f_id = cc3.f_id;    
    """
    cursor.execute(sql)
    food_nutrients = cursor.fetchall()
    return food_nutrients

## 依其所使用的公克數，得到吃的東西的24種營養素 (食譜版)
def check_recipe(food_name, gram):
    cursor = connection.cursor()
    sql = f"""
    SELECT c2.n_id, c2.per100_content * {gram} / 100 AS "content"
    FROM (
            SELECT r_id, RecipeName FROM i_nutrition.original_recipe WHERE RecipeName LIKE "%{food_name}%" ORDER BY RAND() LIMIT 1
            ) c1
    JOIN i_nutrition.recipe_nutrients_content_per100g_normalization c2
    ON c1.r_id = c2.r_id;   
    """
    cursor.execute(sql)
    recipe_nutrients = cursor.fetchall()
    return recipe_nutrients



## 每次會員填寫完每日錄表後執行，新增按下finish時，所有吃的東西的24種營養素
def do_daily_nutrients(m_id, daily_data):
    food_list = daily_data[0]   # 使用者當日吃的所有食物 (多項)
    gram_list = daily_data[1]   # 使用者當日吃的所有食物各自的公克重 (多項)


    cursor = connection.cursor()
    sql_open = """
    SET SQL_SAFE_UPDATES=0;
    """
    cursor.execute(sql_open)        #開啟SQL修改功能

    for food_name, gram in zip(food_list, gram_list):
        food_nutrients = check_food(food_name, gram)

        if food_nutrients != ():
            for f_n_item in food_nutrients:
                sql = f"""
                INSERT INTO for_foodgroup.daily_nutrients
                (record_time, m_id, n_id, daily_content)
                VALUES
                (CURDATE(), "{m_id}", {f_n_item[0]}, ROUND({f_n_item[1]}, 2));
                """
                cursor.execute(sql)

        else:
            recipe_nutrients = check_recipe(food_name, gram)
            if recipe_nutrients != ():
                for r_n_item in recipe_nutrients:
                    sql = f"""
                    INSERT INTO for_foodgroup.daily_nutrients
                    (record_time, m_id, n_id, daily_content)
                    VALUES
                    (CURDATE(), "{m_id}", {r_n_item[0]}, ROUND({r_n_item[1]}, 2));
                    """
                    cursor.execute(sql)

            else:
                pass

    connection.commit()
    sql_close = """
    SET SQL_SAFE_UPDATES=1;
    """
    cursor.execute(sql_close)           #關閉指令
    cursor.close()
    print("daily_nutrients load success!")



"""##########################################################################
    範例資訊
        # m_id = "M10000001"
        # daily_data = (["橘子", "牛奶麵包", "香蕉", "咖哩飯"], [100, 150, 120, 300])
        # do_daily_nutrients(m_id, daily_data)
##########################################################################"""

