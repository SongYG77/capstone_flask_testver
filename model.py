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

    def __init__(self,id,password,name,address,sex):
        self.id = id
        self.password = password
        self.name = name
        self.address = address
        self.sex = sex



class Bench(db.Model):
    __tablename__ = "bench"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(32))
    date = db.Column(db.String(32))
    time = db.Column(db.String(32))

    def __init__(self,id,name,date,time):
        self.id = id
        self.name = name
        self.date = date
        self.time = time

class Reck(db.Model):
    __tablename__ = "reck"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(32))
    date = db.Column(db.String(32))
    time = db.Column(db.String(32))

    def __init__(self,id,name,date,time):
        self.id = id
        self.name = name
        self.date = date
        self.time = time

class Aerobic(db.Model):
    __tablename__ = "Aerobic"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(32))
    date = db.Column(db.String(32))
    time = db.Column(db.String(32))

    def __init__(self,id,name,date,time):
        self.id = id
        self.name = name
        self.date = date
        self.time = time



