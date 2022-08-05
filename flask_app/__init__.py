from flask import Flask, render_template, Blueprint, jsonify, request
from flask_app.routes.main_route import bp as main_bp
import pickle
import sqlite3
import os

app = Flask(__name__, static_url_path = '/static')
app.register_blueprint(main_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == "POST":
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        cp = int(request.form['cp'])
        trtbps = int(request.form['trtbps'])
        chol = int(request.form["chol"])
        fbs = int(request.form["fbs"])
        restecg = int(request.form["restecg"])
        thalachh = int(request.form["thalachh"])
        
        model = None
        with open('/Users/lje/RealTimeER/flask_app/model.pkl','rb') as pickle_file:
            model = pickle.load(pickle_file)
        X_test = [[age, sex, cp, trtbps, chol, fbs, restecg, thalachh]]
        y_pred = model.predict(X_test)[0]

        if y_pred == 0:
            y_pred = "심장마비일 가능성이 50% 이하 입니다."
        else:
            y_pred = "심장마비일 가능성이 50% 이상 입니다."

        return render_template('index4.html', y_pred=y_pred)
    else:
        return render_template('index4.html')

@app.route('/table', methods=["GET", "POST"])
def table():
    if request.method == "POST":
        sido = request.form['sido']
        sigungu = request.form['sigungu']

        conn = sqlite3.connect('/Users/lje/RealTimeER/project.db')
        cur = conn.cursor()
        cur.execute(f"SELECT Sido, Sigungu, Datetime, Hpname, Ercall, Erwards, Orwards, Ct, Mri, Vent, Icuwards, Ccuwards FROM ER_table WHERE Sido='{sido}' AND Sigungu='{sigungu}';")
        rows = [r for r in cur.fetchall()]

        return render_template('index5.html', rows=rows, sido=sido, sigungu=sigungu)
    else:
        return render_template('index5.html')


if __name__ == "__main__":
    app.run(debug=True)