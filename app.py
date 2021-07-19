from flask      import Flask, jsonify, request
import pymysql
app = Flask(__name__)

def db_connector():
    db = pymysql.connect(
        host='',
        port=3306,
        user='',
        passwd='',
        db='capdb',
        charset='utf8')
    cursor = db.cursor()
    sql = '''SELECT * FROM capstone;'''
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return str(result)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/dbconnect")
def dbtest():
    a = db_connector()
    return a

if __name__ == '__main__' :
    app.run(debug = False, host = '0.0.0.0')

