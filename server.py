import sys
import jsonify
from flask import Flask, session, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from models import User, Dotfile
from utils import generateRandomString

# App configuration ====
app = Flask('GPGdotgetter')
app.config['DATABASE_FILE'] = 'GPGdotgetter_DB.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GPGdotgetter_DB.sqlite'
app.secret_key = "CHANGE_ME"
# ======================
db = SQLAlchemy(app)
SESSIONID_SIZE = 256


# decorators ===========
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if(session.get('logged_in')):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap


# ======================
# routes ===============
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# ================
# routes.api =====
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    session.pop('logged_in', False)
    return redirect(url_for('home'))


@login_required
@app.route('/api/login', methods=['POST'])
def API_login():
    response = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        q = User.query.filter_by(email=email).first()
        if len(email) < 3 or len(password) < 8 or not q:
            response = jsonify({
                'code': 401,
                'message': 'Email or password incorrect'
            })
        elif check_password_hash("pbkdf2:sha512:131072$" + q.password, password):
            session['logged_in'] = True
            response = jsonify({
                'code': 200,
                'message': 'Success',
                'sessionID': generateRandomString(SESSIONID_SIZE),
                'logged_in': True
            })
        else:
            response - jsonify({
                'code': 501,
                'message': 'Server cannot interpret that email or password'
            })
    else:
        response = jsonify({
            'code': 405,
            'message': 'Only POST request allowed'
        })
    return response


@app.route('/api/register', methods=['POST'])
def API_register():
    response = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        rpassword = request.form['rpassword']
        if len(email) < 3 or len(password) < 8:
            return jsonify({
                'code': 422,
                'message': 'Minimal length of password is 8, minimal length of email is 4'
            })
        q = User.query.filter_by(email=email).first()  # return None if nothing got selected
        if not q:
            return jsonify({
                'code': 400,
                'message': 'That email is already registred'
            })
        elif rpassword != password:
            return jsonify({
                'code': 400,
                'message': 'Passwords don\'t match'
            })
        u = User(
                email=email,
                password=generate_password_hash(
                    password,
                    method="pbkdf2:sha512:131072"
                ),
                validated=False
            )
        db.session.add(u)
        db.session.commit()
        response = jsonify({
            'code': 201,
            'message': 'Created new account'
        })
    else:
        response = jsonify({
            'code': 405,
            'message': 'Only POST request allowed'
        })
    return response


# ======================
def StartServer():
    print("helloworld")


if __name__ == '__main__':
    print("Please run main.py to start server")
    sys.exit(1)
