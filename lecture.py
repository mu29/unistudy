#-*- coding: utf-8 -*-

from flask import *
from database import db
from server import app

@app.route('/lecture/<subject>')
def lecture(subject):
    return render_template('lecture.html', subject=subject)