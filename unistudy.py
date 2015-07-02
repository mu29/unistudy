from flask import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
