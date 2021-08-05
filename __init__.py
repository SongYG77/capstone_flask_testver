from model import db, User, Bench, Reck
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
