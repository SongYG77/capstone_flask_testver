from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user_table"
    id_num = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(32))
    name = db.Column(db.String(32))
    address = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    start_date = db.Column(db.String(45))
    end_date = db.Column(db.String(45))
    enrollment = db.Column(db.String(45))

    def __init__(self,id,password,name,address,sex,start_date,end_date,enrollment):
        self.id = id
        self.password = password
        self.name = name
        self.address = address
        self.sex = sex
        self.start_date = start_date
        self.end_date = end_date
        self.enrollment = enrollment



class Bench(db.Model):
    __tablename__ = "bench"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.String(32))
    date = db.Column(db.String(32))
    start_time = db.Column(db.String(32))
    end_time = db.Column(db.String(32))

    def __init__(self,id,userid,date,start_time,end_time):
        self.id = id
        self.userid = userid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Reck(db.Model):
    __tablename__ = "reck"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.String(32))
    date = db.Column(db.String(32))
    start_time = db.Column(db.String(32))
    end_time = db.Column(db.String(32))

    def __init__(self, id, userid, date, start_time, end_time):
        self.id = id
        self.userid = userid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Aerobic(db.Model):
    __tablename__ = "aerobic"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.String(32))
    date = db.Column(db.String(32))
    start_time = db.Column(db.String(32))
    end_time = db.Column(db.String(32))

    def __init__(self, id, userid, date, start_time, end_time):
        self.id = id
        self.userid = userid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time