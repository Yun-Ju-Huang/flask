from sqlalchemy import create_engine
import pymysql

def acount():   # 套件 sqlalchemy 時使用
    host = "35.229.172.113"
    port = 3306
    user = "food3"
    password = "mysqlfoodeb101"
    db = "i_nutrition"
    engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}?charset=utf8')
    return engine

def acount2():  # 套件 pymysql 時使用
    host = "35.229.172.113"
    port = 3306
    user = "food3"
    password = "mysqlfoodeb101"
    db = "i_member"
    connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset="utf8")
    cursor = connection.cursor()
    return cursor

def login():
    user = "food3"
    password = "mysqlfoodeb101"
    host = "35.229.172.113"
    return user, password, host
