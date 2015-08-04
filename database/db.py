# -*- coding: utf-8 -*-

from flaskext.mysql import MySQL
from server import app

class DataBase:

    def __init__(self):
        self.mysql = MySQL()
        self.mysql.init_app(app)

    def get_mysql(self):
        return self.mysql

db = DataBase()
