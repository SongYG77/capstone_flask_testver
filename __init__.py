from model import db, User, Bench, Reck,Aerobic
from flask import Flask, render_template, request, redirect , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)


@app.route('/reservation',methods=['GET','POST'])
def reserve():
    if request.method == 'GET':
        b = []
        data = Bench.query.all()
        print(data)
        for i in data:
            a = {"datetime" :i.date+" "+i.time,
                 "name": i.name}
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        name = params['name']
        date = params['date']
        time = params['time']

        bench = Bench(id, name, date, time)
        db.session.add(bench)
        db.session.commit()
        return 'OK'

@app.route('/bench_reservation_user/<username>',methods=['GET','POST'])
def benchreserve_user(username):
    if request.method == 'GET' :

        bench = []
        benchdata = Bench.query.filter(Bench.name == username).all()
        for i in benchdata:
            a = {"datetime" :i.date+" "+i.time,
                 "name": i.name}
            bench.append(a)
        return jsonify(bench)

@app.route('/reck_reservation_user/<username>',methods=['GET','POST'])
def reckreserve_user(username):
    if request.method == 'GET' :
        reck = []
        reckdata = Reck.query.filter(Reck.name == username).all()
        for i in reckdata:
            a = {"datetime": i.date + " " + i.time,
                 "name": i.name}
            reck.append(a)

        return jsonify(reck)

@app.route('/aerobic_reservation_user/<username>',methods=['GET','POST'])
def aerobicreserve_user(username):
    if request.method == 'GET' :
        aerobic = []
        aerobicdata = Aerobic.query.filter(Aerobic.name == username).all()
        for i in aerobicdata:
            a = {"datetime": i.date + " " + i.time,
                 "name": i.name}
            aerobic.append(a)

        return jsonify(aerobic)

if __name__ == "__main__":
    migrate = Migrate()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:thddbs00@localhost:3306/capstone'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.app = app
    db.create_all()
    migrate.init_app(app, db)
    app.run(debug = False, host = '0.0.0.0')
#기구별로 나눠서 저장되게 바꾸기.
