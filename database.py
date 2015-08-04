#-*- coding: utf-8 -*-

import MySQLdb
from flaskext.mysql import MySQL
from server import app

class DataBase():

    # 커넥션 맺자
    def __init__(self):
        self.mysql = MySQL()
        self.mysql.init_app(app)
        self.connection = self.mysql.connect()
        self.connection.autocommit(True)

    # 쿼리 실행
    def execute(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)

        return cursor


db = DataBase()