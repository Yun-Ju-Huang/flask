from flask import Flask, render_template
app=Flask(__name__)
@app.route('/login')
def login_try():
    return render_template('login_try.html')
@app.route('/create')
def create():
    return render_template('create_new_account.html')

@app.route('/click')
def click():
    return render_template('click.html')



@app.route('/home')
def home():
    return render_template('home_try.html')





if __name__ == '__main__':
    app.run(debug=True)