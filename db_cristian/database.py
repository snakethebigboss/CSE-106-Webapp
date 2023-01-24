import sqlite3
from sqlite3 import Error
from flask import Flask
from flask_restful import Api, Resource, reqparse
import flask_login

app = Flask(__name__)
with app.app_context():
    api = Api(app)
    db = r"tpch.sqlite"
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    
    class ACME_Univeristy(Resource):
        def get(self):
            sql = """select * from users"""

            try:
                c = conn.cursor()
                c.execute(sql)

            except Error as e:
                print(e)

            return c.fetchall()
            
        def post(self):
            pass
        def put(self):
            pass
        def delete(self):
            pass

    if __name__ == '__main__':
        app.run(debug=True)