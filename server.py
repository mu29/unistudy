#-*- coding: utf-8 -*-

from flask import *
from load_modules import MODULE_NAMES

app = Flask(__name__)

app.secret_key = 'secretkey'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'projectDanbi'
app.config['MYSQL_DATABASE_DB'] = 'unistudy'

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/lecture/<subject>')
def lecture(subject):
    return render_template('lecture.html', subject=subject)

def init_server():
    for module_name in MODULE_NAMES:
        __import__(module_name)