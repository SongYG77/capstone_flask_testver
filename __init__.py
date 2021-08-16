from model import db, User, Bench, Reck,Aerobic,test_Table
from flask import Flask, render_template, request, redirect , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import schedule
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

pymysql.install_as_MySQLdb()
app = Flask(__name__)

#바뀐 작업 : 데베 스키마 변경 그래서 모델에서 start,end time 수정 aerobic 소문자로
#아래 reservation_user 추가
#스캐쥴 추가. apscheduler 사용(pip 설치 필요)
#date 파트로 오늘 날짜보다 전일 예약이면 삭제하도록 만듬
#그럴려면 데베 스키마를 date 파트 전부 date 형으로 변경해야함.
#import time 이랑 datetime 추가.
#유저 정보 부르는 기등 추가.

#background 방식으로 사용해야 start 이후 중지되지 않음
sched = BackgroundScheduler()
#지금은 테스트를 위해 매 분 갱신 이후에는('cron', hour='0', minute='10', id='update_db') 0시 10분에 갱신되도록 바꿀 예정
@sched.scheduled_job('cron', second = '0', id='test')
def test():
    test_Table.query.filter(test_Table.date < datetime.date.today()).delete()
    db.session.commit()

#스캐쥴링 시작. 실행되고 있는 동안 스캐쥴에 의해 실행될 것.
sched.start()

#예약 정보를 받고 보내는 부분(기구별로 나눔)
@app.route('/bench_reservation',methods=['GET','POST'])
def reserve():
    if request.method == 'GET':
        b = []
        data = Bench.query.all()
        for i in data:
            a = {
                "date": i.date,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                 "name": i.name
                 }
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        name = params['name']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        bench = Bench(id, name, date, start_time, end_time)
        db.session.add(bench)
        db.session.commit()
        return 'OK'

@app.route('/reck_reservation',methods=['GET','POST'])
def reserve():
    if request.method == 'GET':
        b = []
        data = Reck.query.all()
        for i in data:
            a = {
                "date": i.date,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                 "name": i.name
                 }
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        name = params['name']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        reck = Reck(id, name, date, start_time, end_time)
        db.session.add(reck)
        db.session.commit()
        return 'OK'

@app.route('/aerobic_reservation',methods=['GET','POST'])
def reserve():
    if request.method == 'GET':
        b = []
        data = Aerobic.query.all()
        for i in data:
            a = {
                "date": i.date,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                 "name": i.name
                 }
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        name = params['name']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        aerobic = Aerobic(id, name, date, start_time, end_time)
        db.session.add(aerobic)
        db.session.commit()
        return 'OK'

#유저 마이페이지 부분, 사용자의 예약 정보를 불러옴.
@app.route('/reservation_user/<username>',methods=['GET','POST'])
def reservation_user(username):
    if request.method == 'GET':

        reservelist = []

        benchdata = Bench.query.filter(Bench.name == username).all()
        reckdata = Reck.query.filter(Reck.name == username).all()
        aerobicdata = Aerobic.query.filter(Aerobic.name == username).all()

        for i in benchdata:
            temp = {
                "equipment" : "bench",
                "date": i.date,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                 "name": i.name
            }
            reservelist.append(temp)
        for i in reckdata:
            temp = {
                "equipment" : "reck",
                "date": i.date,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                 "name": i.name
            }
            reservelist.append(temp)
        for i in aerobicdata:
            temp = {
                "equipment" : "aerobic",
                "date": i.date,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                 "name": i.name
            }
            reservelist.append(temp)

        return jsonify(reservelist)

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
#유저 정보를 불러오는 부분
@app.route('/userdata/<username>',methods=['GET','POST'])
def getUserData(username):
    if request.method == 'GET' :
        data = User.query.filter(User.name == username).all()
        temp = []
        for i in data:
            a = {'name' : i.name, 'start_date' : i.start_date, 'end_date' : i.end_date, 'enrollment' : i.enrollment}
            temp.append(a)
        return jsonify(temp)
if __name__ == "__main__":
    migrate = Migrate()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:thddbs00@localhost:3306/capstone'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.app = app
    db.create_all()
    migrate.init_app(app, db)
    app.run(debug = False, host = '0.0.0.0')

