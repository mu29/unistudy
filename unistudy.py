#-*- coding: utf-8 -*-

from flask import *
from flaskext.mysql import MySQL
import MySQLdb

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
    cursor.execute("SELECT * FROM `user` WHERE `email` = '" + email + "' AND `password` = '" + password + "';")

    # 유저가 없을 경우
    if cursor.rowcount == 0:
        return u'아이디와 비밀번호를 확인하세요.'

    # 유저를 얻자
    userdata = cursor.fetchone()

    # 인증이 안된 경우
    if userdata['verify'] == 0:
        return u'가입 인증 메일을 확인해주세요.'
    # 밴 된 아이디일 경우
    if userdata['ban'] == 1:
        return u'차단된 계정입니다.'

    # 로그인 성공
    return None


@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
