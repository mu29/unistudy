#-*- coding: utf-8 -*-
'''
import MySQLdb
import smtplib
import hashlib
from flask import *
from flaskext.mysql import MySQL
from email.mime.text import MIMEText

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'projectDanbi'
app.config['MYSQL_DATABASE_DB'] = 'unistudy'
app.secret_key = 'secretkey'

mysql.init_app(app)

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        error = do_login(request.form['email'], request.form['password'])
        if error is None:
            session['email'] = request.form['email']
            return redirect(url_for('index'))

    return render_template('login.html', error=error)


@app.route('/logout/')
def logout():
    session.pop('email', None)
    return render_template('login.html')

def do_login(email, password):
    # 아이디와 비밀번호로 유저 검색
    cursor = mysql.connect().cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM `users` WHERE `email` = '" + email +
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
    cursor.close()
    return None


@app.route('/register/', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        error = do_register(request.form['email'], request.form['password'], request.form['nickname'])
        if error is None:
            return redirect(url_for('login'))

    return render_template('register.html', error=error)

def do_register(email, password, nickname):
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    # 이메일 중복 확인
    cursor.execute("SELECT * FROM `users` WHERE `email` = '" + email + "';")
    if cursor.rowcount > 0:
        cursor.close()
        return u'이미 가입된 메일 주소입니다.'

    # 닉네임 중복 확인
    cursor.execute("SELECT * FROM `users` WHERE `nickname` = '" + nickname + "';")
    if cursor.rowcount > 0:
        cursor.close()
        return u'이미 존재하는 닉네임입니다.'

    # 가입 성공. 메일 보내자
    cursor.execute("INSERT INTO `users` SET `email` = '" + email +
                   "', `password` = '" + hashlib.sha224(password).hexdigest() +
                   "', `nickname` = '" + nickname + "';")
    cursor.close()
    conn.commit()
    send_success_mail(email)
    return None

def send_success_mail(email):
    verify_key = hashlib.sha224(email + app.secret_key).hexdigest()
    msg = MIMEText('http://0.0.0.0/verify/?email=' + email + '&key=' + verify_key)

    msg['Subject'] = u'유니스터디 가입 인증 메일입니다.'
    msg['From'] = 'unistylemaster@gmail.com'
    msg['To'] = email

    # 로컬 SMTP 서버가 없을 경우 계정이 있는 다른 서버를 사용하면 된다.
    s = smtplib.SMTP_SSL('smtp.gmail.com',465)
    s.login('unistylemaster@gmail.com', 'password')
    s.sendmail('unistylemaster@gmail.com', email, msg.as_string())
    s.quit()

@app.route('/verify/', methods=['POST', 'GET'])
def verify():
    if request.method == 'GET':
        email = request.args['email']
        verify_key = hashlib.sha224(email + app.secret_key).hexdigest()
        if verify_key == request.args['key']:
            conn = mysql.connect()
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE `users` SET `verify` = '1' WHERE `email` = '" + email + "';")
            conn.commit()
            session['email'] = request.form['email']
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/lecture/<subject>')
def lecture(subject):
    return render_template('lecture.html', subject=subject)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')'''