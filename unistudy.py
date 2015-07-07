from flask import *
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'projectDanbi'
app.config['MYSQL_DATABASE_DB'] = 'unistudy'

mysql.init_app(app)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if do_login(request.form['email'], request.form['password']):
            session['email'] = request.form['email']
            return redirect(url_for('index'))
    return render_template('login.html')

def do_login(email, password):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM `user` WHERE `email` = '" + email + "' AND `password` = '" + password + "';")

    if len(cursor.fetchall()) > 0:
        return True
    return False


@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
