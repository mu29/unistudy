# -*- coding: utf-8 -*-

from flask import *
from server import app
from database.lecture_db import lecture_db


@app.route('/lecture/<no>')
def lecture(no):
    # content = Markup(markdown.markdown(content))

    if 'email' not in session:
        return redirect(url_for('login'))

    no = int(no)
    subject_id = lecture_db.subject_list[no]['id']
    return render_template('lecture.html', subject_info=lecture_db.subject_list[no],
                           lecture_info=lecture_db.get_lectures(subject_id))
