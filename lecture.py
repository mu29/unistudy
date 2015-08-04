# -*- coding: utf-8 -*-

from flask import *
from server import app

@app.route('/lecture/<subject>')
def lecture(subject):
    #content = Markup(markdown.markdown(content))
    return render_template('lecture.html', subject=subject)