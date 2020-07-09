from sqlalchemy import create_engine
import pymysql

def acount():   # 套件 sqlalchemy 時使用
    host = "35.229.172.113"
    port = 3306
    user = "food2"
    password = "1234"
    db = "i_nutrition"
    engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}?charset=utf8')
    return engine

def acount2():  # 套件 pymysql 時使用
    host = "35.229.172.113"
    port = 3306
    user = "food2"
    password = "1234"
    db = "i_member"
    connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset="utf8")
    cursor = connection.cursor()
    return cursor

def login():
    user = "food2"
    password = "1234"
    return user, password
