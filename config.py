db = {
    'user'     : 'capstone',
    'password' : 'capstones',
    'host'     : 'capdb.c8wz24ghmr8c.us-east-2.rds.amazonaws.com',
    'port'     : '3306',
    'database' : 'capdb'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"