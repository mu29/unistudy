# -*- coding: utf-8 -*-

import hashlib
import smtplib
from email.mime.text import MIMEText
from flask import *
from database.user_db import user_db
from server import app

@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    # POST : 로그인 시도
    if request.method == 'POST':
        error = user_db.login(request.form['email'], request.form['password'])
        if error is None:
            return redirect(url_for('index'))

    # GET : 로그인 페이지
    return render_template('login.html', error=error)


@app.route('/logout/')
def logout():
    session.pop('email', None)
    return render_template('login.html')


@app.route('/register/', methods=['POST', 'GET'])
def register():
    error = None
    # POST : 가입 시도
    if request.method == 'POST':
        error = user_db.register(request.form['email'], request.form['password'], request.form['nickname'])
        if error is None:
            send_success_mail(request.form['email'])
            return redirect(url_for('login'))

    # GET : 가입 페이지
    return render_template('register.html', error=error)


@app.route('/verify/', methods=['GET'])
def verify():
    email = request.args['email']
    verify_key = hashlib.sha224(email + app.secret_key).hexdigest()
    # 가입 키 일치 여부 확인
    if verify_key == request.args['key']:
        user_db.verify(email)
        session['email'] = request.form['email']
        return redirect(url_for('index'))

    return render_template('register.html')


def send_success_mail(email):
    verify_key = hashlib.sha224(email + app.secret_key).hexdigest()
    msg = MIMEText('http://0.0.0.0:5000/verify/?email=' + email + '&key=' + verify_key)

    msg['Subject'] = u'유니스터디 가입 인증 메일입니다.'
    msg['From'] = 'unistylemaster@gmail.com'
    msg['To'] = email

    # 로컬 SMTP 서버가 없을 경우 계정이 있는 다른 서버를 사용하면 된다.
    s = smtplib.SMTP_SSL('smtp.gmail.com',465)
    s.login('unistylemaster@gmail.com', 'pw')
    s.sendmail('unistylemaster@gmail.com', email, msg.as_string())
    s.quit()
