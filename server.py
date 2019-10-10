import sys
import ast
import datetime
import os
from flask import session, redirect, url_for, render_template, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from db_models import User, Dotfile, app, db
from utils import generateRandomString


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
    session.pop('sessionID', False)
    return redirect(url_for('index'))


@login_required
@app.route('/api/login', methods=['POST'])
def API_login():
    response = None
    if request.method == 'POST':
        try:
            email = ast.literal_eval(request.data.decode('UTF-8'))['email']
            password = ast.literal_eval(request.data.decode('UTF-8'))['password']
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid input'
            })
        q = User.query.filter_by(email=email).first()
        if len(email) < 3 or len(password) < 2 or not q:
            response = jsonify({
                'code': 401,
                'message': 'Email or password incorrect'
            })
        elif check_password_hash(q.password, password):
            session['logged_in'] = True
            session['sessionID'] = generateRandomString(SESSIONID_SIZE)
            response = jsonify({
                'code': 200,
                'message': 'Success',
                'sessionID': session['sessionID']
            })
        else:
            response = jsonify({
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
        try:
            email = ast.literal_eval(request.data.decode('UTF-8'))['email']
            password = ast.literal_eval(request.data.decode('UTF-8'))['password']
            rpassword = ast.literal_eval(request.data.decode('UTF-8'))['rpassword']
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid input'
            })
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
                password=generate_password_hash(password, method="pbkdf2:sha512:131072"),
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
    app_dir = os.path.realpath(os.path.dirname(__file__))
    db_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(db_path):
        build_db()
    app.run(host='0.0.0.0', debug=True)


def build_db():
    print("================CREATING TEST DB================")
    db.create_all()
    u = User(
        email="test@test.com",
        password=generate_password_hash("test", method="pbkdf2:sha512:131072"),
        validated=False
    )
    d1 = Dotfile(createdOn=datetime.datetime.now(), password="testpass")
    d2 = Dotfile(createdOn=datetime.datetime.now(), password="testpass2")
    u.dotfiles.extend([d1, d2])
    db.session.add(u)
    db.session.add_all([d1, d2])
    db.session.commit()


if __name__ == '__main__':
    print("Please run main.py to start server")
    sys.exit(1)
