import  requests,re,json,pymysql
from flask import Flask ,redirect , render_template,request
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  ##設置瀏覽器不緩存
# @app.route('/user/<name>')
# def user(name):
#     return f'<h1>Hello {name}!!</h1>'
#
# @app.route('/')
# def index4():
#     return redirect('https://www.google.com.tw/')
#
@app.route("/drinks/<item>")
def doostrap(item):
    drinks = ['Coffee', 'Coke', 'Green Tea', 'Water']
    return render_template('bootstrap.html', url_input=item, drinks=drinks)
#登入
# @app.route('/home/loginurl', methods=['GET', 'POST'])
# def login():
#
#     return render_template('login.html')

@app.route("/login")
def login():

    return render_template('login.html',login= "https://google.com")

@app.route("/test")
def test():

    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True)
