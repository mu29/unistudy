#-*- coding: utf-8 -*-

import hashlib
import smtplib
from flask import *
from database import db
from server import app
from email.mime.text import MIMEText

@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    # POST : 로그인 시도
    if request.method == 'POST':
        error = do_login(request.form['email'], request.form['password'])
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
        error = do_register(request.form['email'], request.form['password'], request.form['nickname'])
        if error is None:
            return redirect(url_for('login'))

    # GET : 가입 페이지
    return render_template('register.html', error=error)


@app.route('/verify/', methods=['GET'])
def verify():
    email = request.args['email']
    verify_key = hashlib.sha224(email + app.secret_key).hexdigest()
    # 가입 키 일치 여부 확인
    if verify_key == request.args['key']:
        cursor = db.execute("UPDATE `users` SET `verify` = '1' WHERE `email` = '" + email + "';")
        cursor.close()
        session['email'] = request.form['email']
        return redirect(url_for('index'))

    return render_template('register.html')


def do_login(email, password):
    # 아이디와 비밀번호로 유저 검색
    cursor = db.execute("SELECT * FROM `users` WHERE `email` = '" + email +
                        "' AND `password` = '" + hashlib.sha224(password).hexdigest() + "';")

    # 유저가 없을 경우
    if cursor.rowcount == 0:
        cursor.close()
        return u'아이디와 비밀번호를 확인하세요.'

    # 유저를 얻자
    userdata = cursor.fetchone()

    # 인증이 안된 경우
    if userdata['verify'] == 0:
        cursor.close()
        return u'가입 인증 메일을 확인해주세요.'

    # 밴 된 아이디일 경우
    if userdata['ban'] == 1:
        cursor.close()
        return u'차단된 계정입니다.'

    # 로그인 성공
    session['nickname'] = userdata['nickname']
    session['email'] = userdata['email']
    cursor.close()

def do_register(email, password, nickname):
    cursor = db.execute("SELECT * FROM `users` WHERE `email` = '" + email + "';")
    if cursor.rowcount > 0:
        cursor.close()
        return u'이미 가입된 메일 주소입니다.'

    # 닉네임 중복 확인
    cursor.close()
    cursor = db.execute("SELECT * FROM `users` WHERE `nickname` = '" + nickname + "';")
    if cursor.rowcount > 0:
        cursor.close()
        return u'이미 존재하는 닉네임입니다.'

    # 가입 성공. 메일 보내자
    cursor.close()
    cursor = db.execute("INSERT INTO `users` SET `email` = '" + email +
                        "', `password` = '" + hashlib.sha224(password).hexdigest() +
                        "', `nickname` = '" + nickname + "';")

    cursor.close()
    send_success_mail(email)
    return None

def send_success_mail(email):
    verify_key = hashlib.sha224(email + app.secret_key).hexdigest()
    msg = MIMEText('http://0.0.0.0:5000/verify/?email=' + email + '&key=' + verify_key)

    msg['Subject'] = u'유니스터디 가입 인증 메일입니다.'
    msg['From'] = 'unistylemaster@gmail.com'
    msg['To'] = email

    # 로컬 SMTP 서버가 없을 경우 계정이 있는 다른 서버를 사용하면 된다.
    s = smtplib.SMTP_SSL('smtp.gmail.com',465)
    s.login('unistylemaster@gmail.com', 'rmatn11!')
    s.sendmail('unistylemaster@gmail.com', email, msg.as_string())
    s.quit()