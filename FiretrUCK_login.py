from flask import Flask, url_for, request, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_bootstrap import Bootstrap
import flask_bcrypt
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)
#  會使用到session，故為必設。  
app.secret_key = 'Your Key'
login_manager = LoginManager(app)
#  login\_manager.init\_app(app)也可以

#  假裝是我們的使用者  
users = {'XXX@gmail.com': {'password':'$2b$05$omfOnTlGYnByY9vhhyMceuJa0RIzmGoMTkbfT2tRHJ8qbgBnUTPFG'},
         'aaa@gmail.com':{'password':'$2b$12$/z9RomvXHYD/Zbrv/uvlmeSthIQl8YeemOr/v.u1MoRVIDVMeuzuy'}
         }


class User(UserMixin):
    """  
 設置一： 只是假裝一下，所以單純的繼承一下而以 如果我們希望可以做更多判斷，
 如is_administrator也可以從這邊來加入 
 """

    pass


@login_manager.user_loader
def user_loader(email):
    """  
 設置二： 透過這邊的設置讓flask_login可以隨時取到目前的使用者id   
 :param email:官網此例將email當id使用，賦值給予user.id    
 """
    if email not in users:
        return

    user = User()
    user.id = email
    return user

######################################################################################################
@app.route('/login_try', methods=['GET', 'POST'])
def login_try():
    if request.method == 'GET':
        return render_template("login_try.html")
    email = request.form['email']

    if email not in users:
        flash("登入失敗!!!請確認帳號是否正確!!!")
        return redirect(url_for('login_try'))
    else:
        if flask_bcrypt.check_password_hash(users[email]['password'], request.form['password']) == True:
            #  實作User類別
            user = User()
            #  設置id就是email
            user.id = email
            #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。
            login_user(user)
            #  登入成功，轉址
            return redirect(url_for('success'))

        else:
            flash("登入失敗!!!請確認密碼是否正確!!!")
            return redirect(url_for('login_try')) # 密碼錯誤


@app.route('/success', methods=['GET', 'POST'])
@login_required
def success():
    user = current_user.id
    return render_template("success.html", user=user)


@app.route('/logout')
def logout():
    """
 logout\_user會將所有的相關session資訊給pop掉
 """
    logout_user()
    return redirect(url_for('login_try'))

# @app.errorhandler(401)
# def custom_401(error):
#     return redirect(url_for('login_try'))
#####################################################################################################
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """
#  官網git很給力的寫了一個login的頁面，在GET的時候回傳渲染
#  """
#     if request.method == 'GET':
#         return '''
#      <form action='login' method='POST'>
#     <input type='text' name='email' id='email' placeholder='email'/>
#      <input type='password' name='password' id='password' placeholder='password'/>
#     <input type='submit' name='submit'/>
#     </form>
#                  '''
#
#     email = request.form['email']
#     if request.form['password'] == users[email]['password']:
#         #  實作User類別
#         user = User()
#         #  設置id就是email
#         user.id = email
#         #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。
#         login_user(user)
#         #  登入成功，轉址
#         return redirect(url_for('protected'))
#
#     return 'Bad login'
#
# @app.route('/protected')
# @login_required
# def protected():
#     """
#  在login_user(user)之後，我們就可以透過current_user.id來取得用戶的相關資訊了
#  """
#     #  current_user確實的取得了登錄狀態
#     if current_user.is_active:
#
#         return 'Logged in as: ' + current_user.id + 'Login is_active:True'
#
#
# @app.route('/logout')
# def logout():
#     """
#  logout\_user會將所有的相關session資訊給pop掉
#  """
#     logout_user()
#     return 'Logged out'


if __name__ == '__main__':
    app.run(debug=True)

    # port = int(os.environ.get('PORT', 5000))
    # app.run(debug=True,port=port,host="0.0.0.0")