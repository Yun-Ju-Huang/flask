from flask import Flask, render_template, request, redirect, url_for
import flask_to_mysql2 as ftm2
import pandas as pd
import datetime

app = Flask(__name__)

occupied = False

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index4.html')


@app.route('/history_select', methods=['GET', 'POST'])
def history_query():
    if request.method == 'POST':
        datestart = request.form.get('datestart')
        dateend = request.form.get('dateend')

        datestart_k = str(datetime.datetime.strptime(datestart, "%Y-%m-%dT%H:%M"))
        dateend_k = str(datetime.datetime.strptime(dateend, "%Y-%m-%dT%H:%M"))
        datestart_k = datestart_k[0:10]+'T'+ datestart_k[11:19]
        dateend_k = dateend_k[0:10] + 'T' + dateend_k[11:19]

        # 送入ftm2函式，去Mysql抓資料
        datestart_sql = datestart.replace('T',' ')
        dateend_sql = dateend.replace('T',' ')
        result_list = ftm2.sqlselect(datestart_sql, dateend_sql)
        data_org = result_list[0]
        data_count = result_list[1]

        # 把dataframe變成html
        pd.set_option('colheader_justify', 'center')
        sqldata2 = pd.DataFrame.to_html(data_org, header=True)
        # html存檔
        sqldata_file = open(r"C:\Users\Big data\Documents\GitHub\SMart\SMart\static\sqldata2.html", "w")
        sqldata_file.write(sqldata2)
        sqldata_file.close()

        return render_template('transaction3.html', tables=[data_org.to_html(classes='data')], data_count=data_count,
                               datestart_sql=datestart_sql, dateend_sql=dateend_sql, datestart_k = datestart_k, dateend_k = dateend_k)

    else:
        return render_template('history_select.html')


@app.route('/realtime', methods=['GET', 'POST'])
def realtime():
    return render_template('realtime.html')


@app.route('/rfm', methods=['GET', 'POST'])
def rfm():
    return render_template('rfm.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)