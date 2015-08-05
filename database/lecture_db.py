# -*- coding: utf-8 -*-

import MySQLdb
import markdown
from flask import Markup
from database.db import *
from server import app


class LectureDB:

    def __init__(self):
        self.connection = db.get_mysql().connect()
        self.connection.autocommit(True)
        self.subject_list = self.get_subjects()

    def get_subjects(self):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM `subjects`;")
        subject_list = cursor.fetchall()
        cursor.close()

        for subject in subject_list:
            subject['message'] = Markup(markdown.markdown(subject['message']))

        return subject_list

    def get_lectures(self, subject_id):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM `lectures` WHERE `subject_id` = " + str(subject_id) + ";")
        lecture_list = cursor.fetchall()
        cursor.close()

        return lecture_list


lecture_db = LectureDB()


@app.template_global()
def subjects():
    return lecture_db.subject_list


@app.template_global()
def get_length(item):
    return len(item)
