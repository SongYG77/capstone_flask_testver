from model import db, User, Bench, Reck, Aerobic, Ptclass
from flask import Flask, render_template, request, redirect, jsonify,Response, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended import *
import json
from datetime import datetime

app = Flask(__name__)

# background 방식으로 사용해야 start 이후 중지되지 않음
sched = BackgroundScheduler()

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = 'example secret key'
)
jwt = JWTManager(app)


# 지금은 테스트를 위해 매 분 갱신 이후에는('cron', hour='0', minute='10', id='update_db') 0시 10분에 갱신되도록 바꿀 예정
@sched.scheduled_job('cron', hour='0', minute='10', id='update_db')
def update_db():
    # Bench.query.filter(datetime.datetime.strptime(Bench.date, "%Y-%m-%d").date() < datetime.date.today()).delete()
    # Reck.query.filter(datetime.datetime.strptime(Reck.date, "%Y-%m-%d").date() < datetime.date.today()).delete()
    # Aerobic.query.filter(datetime.datetime.strptime(Aerobic.date, "%Y-%m-%d").date() < datetime.date.today()).delete()
    db.session.commit()


# 스캐쥴링 시작. 실행되고 있는 동안 스캐쥴에 의해 실행될 것.
sched.start()

#로그인 구현중
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' :
        params = request.get_json()
        userid = params['userid']
        password = params['password']

        data = User.query.filter((userid == User.id) & (password == User.password)).first()
        if data != None :
            resualt = {
                "resualt" : 'OK',
                "access_token" : create_access_token(identity=userid , expires_delta=False)
            }
            return jsonify(resualt)
        else :
            resualt = {
                "resualt" : 'Fail'
            }
            return jsonify(resualt)


# 예약 정보를 받고 보내는 부분(기구별로 나눔)
@app.route('/bench_reservation', methods=['GET', 'POST'])
def reserve_bench():
    if request.method == 'GET':
        b = []
        data = Bench.query.all()
        for i in data:
            a = {
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        userid = params['userid']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        bench = Bench(id, userid, date, start_time, end_time)
        db.session.add(bench)
        db.session.commit()
        return 'OK'


@app.route('/aerobic_reservation', methods=['GET', 'POST'])
def reserve_aerobic():
    if request.method == 'GET':
        b = []
        data = Aerobic.query.all()
        for i in data:
            a = {
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        userid = params['userid']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        aerobic = Aerobic(id, userid, date, start_time, end_time)
        db.session.add(aerobic)
        db.session.commit()
        return 'OK'


@app.route('/reck_reservation/<date>', methods=['GET', 'POST'])
def reserve_reck(date):
    if request.method == 'GET':
        start_lst_hour = []
        start_lst_min = []
        end_lst_hour = []
        end_lst_min = []
        data = Reck.query.filter(Reck.date == date).all()
        for i in data:

            start_lst_hour.append(i.start_time.split(':')[0])
            start_lst_min.append(i.start_time.split(':')[1])
            end_lst_hour.append(i.end_time.split(':')[0])
            end_lst_min.append(i.end_time.split(':')[1])
        a = {
            "start_time_hour": start_lst_hour,
            "start_time_min": start_lst_min,
            "end_time_hour": end_lst_hour,
            "end_time_min": end_lst_min
        }
        return jsonify(a)
    elif request.method == 'POST':
        params = request.get_json()
        userid = params['userid']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        temp = start_time.split(':')
        res_start_time = int(temp[0])*100 + int(temp[1])
        temp = end_time.split(':')
        res_end_time = int(temp[0]) * 100 + int(temp[1])
        return_data = 'OK'
        data = Reck.query.filter(Reck.date == date).all()
        maxid = 0
        for i in data :
            temp = i.start_time.split(':')
            data_stime = int(temp[0])*100 + int(temp[1])
            temp = i.end_time.split(':')
            data_etime = int(temp[0]) * 100 + int(temp[1])

            if maxid<i.id : maxid = i.id
            if res_start_time>=data_stime and res_start_time<=data_etime :
                return_data = 'overlap'
            elif res_end_time>=data_stime and res_end_time<=data_etime :
                return_data = 'overlap'
            elif res_start_time<=data_stime and data_stime<=res_end_time :
                return_data = 'overlap'
            elif i.userid == userid :
                return_data = "overlap_today"

        benchdata = Bench.query.filter( Bench.date == date).filter(Bench.userid == userid).all()
        aerobicdata = Aerobic.query.filter( Aerobic.date == date).filter(Aerobic.userid == userid).all()

        for i in benchdata:
            temp = i.start_time.split(':')
            data_stime = int(temp[0]) * 100 + int(temp[1])
            temp = i.end_time.split(':')
            data_etime = int(temp[0]) * 100 + int(temp[1])
            if res_start_time>=data_stime and res_start_time<=data_etime :
                return_data = 'overlap_user'
            elif res_end_time>=data_stime and res_end_time<=data_etime :
                return_data = 'overlap_user'
            elif res_start_time<=data_stime and data_stime<=res_end_time :
                return_data = 'overlap_user'

        for i in aerobicdata:
            temp = i.start_time.split(':')
            data_stime = int(temp[0]) * 100 + int(temp[1])
            temp = i.end_time.split(':')
            data_etime = int(temp[0]) * 100 + int(temp[1])
            if res_start_time>=data_stime and res_start_time<=data_etime :
                return_data = 'overlap_user'
            elif res_end_time>=data_stime and res_end_time<=data_etime :
                return_data = 'overlap_user'
            elif res_start_time<=data_stime and data_stime<=res_end_time :
                return_data = 'overlap_user'

        if return_data == 'OK' :
            reck = Reck(maxid+1, userid, date, start_time, end_time)
            db.session.add(reck)
            db.session.commit()
        return return_data


# 유저 마이페이지 부분, 사용자의 예약 정보를 불러옴.
@app.route('/reservation_user/<userid>', methods=['GET', 'POST'])
def reservation_user(userid):
    if request.method == 'GET':

        reservelist = []

        benchdata = Bench.query.filter(Bench.userid == userid).all()
        reckdata = Reck.query.filter(Reck.userid == userid).all()
        aerobicdata = Aerobic.query.filter(Aerobic.userid == userid).all()

        for i in benchdata:
            temp = {
                "equipment": "벤치",
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            reservelist.append(temp)
        for i in reckdata:
            temp = {
                "equipment": "파워 렉",
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            reservelist.append(temp)
        for i in aerobicdata:
            temp = {
                "equipment": "유산소",
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            reservelist.append(temp)

        return jsonify(reservelist)


@app.route('/bench_reservation_user/<userid>', methods=['GET', 'POST'])
def benchreserve_user(userid):
    if request.method == 'GET':
        bench = []
        benchdata = Bench.query.filter(Bench.userid == userid).all()
        for i in benchdata:
            a = {"datetime": i.date + " " + i.time,
                 "userid": i.userid}
            bench.append(a)
        return jsonify(bench)


@app.route('/reck_reservation_user/<userid>', methods=['GET', 'POST'])
def reckreserve_user(userid):
    if request.method == 'GET':
        reck = []
        reckdata = Reck.query.filter(Reck.userid == userid).all()
        for i in reckdata:
            a = {"datetime": i.date + " " + i.time,
                 "userid": i.userid}
            reck.append(a)

        return jsonify(reck)


@app.route('/aerobic_reservation_user/<userid>', methods=['GET', 'POST'])
def aerobicreserve_user(userid):
    if request.method == 'GET':
        aerobic = []
        aerobicdata = Aerobic.query.filter(Aerobic.userid == userid).all()
        for i in aerobicdata:
            a = {"datetime": i.date + " " + i.time,
                 "userid": i.userid}
            aerobic.append(a)

        return jsonify(aerobic)


# 유저 정보를 불러오는 부분
@app.route('/userdata/<userid>', methods=['GET', 'POST'])
def getUserData(userid):
    if request.method == 'GET':
        data = User.query.filter(User.id == userid).all()
        temp={}
        for i in data:
            a = {'userid': i.id, 'user_name': i.name, 'start_date': i.start_date, 'end_date': i.end_date,
                 'enrollment': i.enrollment}
            temp=a
        return jsonify(a)

@app.route('/delete/<userid>',methods=['DELETE'])
def delReservation(userid):
    if request.method == 'DELETE':
        name = request.args.get('name')
        date = request.args.get('date')
        reck_user_id = []
        aerobic_user_id = []
        bench_user_id = []
        reck_date =[]
        aerobic_date = []
        bench_date = []
        for i in Reck.query.all():
            reck_user_id.append(i.userid)
            reck_date.append(i.date)
        for i in Aerobic.query.all():
            aerobic_user_id.append(i.userid)
            aerobic_date.append(i.date)
        for i in Bench.query.all():
            bench_user_id.append(i.userid)
            bench_date.append(i.date)

        if name == '파워 렉':
            if userid in reck_user_id and date in reck_date:
                Reck.query.filter((Reck.userid == userid)&(Reck.date == date)).delete()
                db.session.commit()
                return "Reck Delete success"
            else:
                response = Response(status=404)
                return response

        elif name == '유산소':
            if userid in aerobic_user_id and date in aerobic_date:
                Aerobic.query.filter(Aerobic.userid == userid).delete()
                db.session.commit()
                return "Aerobic Delete success"
            else:
                response = Response(status=404)
                return response

        elif name == '벤치':
            if userid in bench_user_id and date in bench_date:
                Bench.query.filter(Bench.userid == userid).delete()
                db.session.commit()
                return "Bench Delete success"
            else:
                response = Response(status=404)
                return response

@app.route('/pt/<userid>',methods=['GET','POST'])
def pt(userid):
    if request.method == 'POST':
        classinfo = request.form['classinfo']
        date = request.form['date']
        user_id = []
        for i in Reck.query.all():
            user_id.append(i.userid)

        if userid in user_id:
            ptclass = Ptclass(id, userid, date, classinfo)
            db.session.add(ptclass)
            db.session.commit()
            return "OK"
        else :
            return 'Fail'
    elif request.method == 'GET':
        date = []
        classinfo =[]
        starttime =[]
        li = []
        todaydate = datetime.today().strftime("%Y-%m-%d")
        a = Ptclass.query.filter((Ptclass.userid == userid)&(Ptclass.date >= todaydate)).order_by('date').all()

        for i in a:
            date.append(i.date)
            classinfo.append(i.classinfo)
            starttime.append(i.starttime)

        for i in range(len(date)):
            dictionary = {'시간' : date[i], '수업 내용' : classinfo[i], '시작 시간': starttime[i]}
            li.append(dictionary)

        pt = {
            'id' : userid,
            'history' : li
        }

        pt_json = json.dumps(pt, ensure_ascii=False)
        res = make_response(pt_json)

        return res


if __name__ == "__main__":
    migrate = Migrate()
    #mysql://root:thddbs00@localhost:3306/capstone
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.app = app
    db.create_all()
    migrate.init_app(app, db)
    app.run(debug = False, host = '0.0.0.0')

