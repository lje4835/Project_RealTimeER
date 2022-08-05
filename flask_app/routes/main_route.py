from flask import Flask, Blueprint, request, jsonify
import pickle

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/', methods=["GET", "POST"])
def get_data():
    if request.method == 'POST':
        age = request.form["age"]
        sex = request.form["sex"]
        cp = request.form["cp"]
        trtbps = request.form["trtbps"]
        chol = request.form["chol"]
        fbs = request.form["fbs"]
        restecg = request.form["restecg"]
        thalachh = request.form["thalachh"]
        pass
    elif request.method == 'GET':
        ## 넘겨받은 숫자 
        age = request.args.get("age")
        sex = request.args.get("sex")
        cp = request.args.get("cp")
        trtbps = request.args.get("trtbps")
        chol = request.args.get("chol")
        fbs = request.args.get("fbs")
        restecg = request.args.get("restecg")
        thalachh = request.args.get("thalachh")

    model = None
    with open('/flask_app/model.pkl','rb') as pickle_file:
        model = pickle.load(pickle_file)
    X_test = [[age, sex, cp, trtbps, chol, fbs, restecg, thalachh]]
    y_pred = model.predict(X_test)

    return y_pred