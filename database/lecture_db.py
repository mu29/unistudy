# -*- coding: utf-8 -*-

import MySQLdb
from database.db import *
from server import app

class LectureDB:

    def __init__(self):
        self.connection = db.get_mysql().connect()
        self.connection.autocommit(True)
        self.subjects = self.get_subjects()

    def get_subjects(self):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM `subjects`;")
        list = cursor.fetchall()
        cursor.close()

        return list


lecture_db = LectureDB()

@app.template_global()
def subjects():
    return lecture_db.subjects

@app.template_global()
def get_length(item):
    return len(item)
