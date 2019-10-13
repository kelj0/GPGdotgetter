import sys
import ast
import datetime
import os
from flask import session, redirect, url_for, render_template, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename
from functools import wraps
from db_models import User, Dotfile, app, db
from utils import generateRandomString, allowed_file


SESSIONID_SIZE = 256
UPLOAD_ROOT =  os.path.join(os.getcwd(),'USER_FILES')
ALLOWED_EXTENSIONS = set(['gpg'])

# decorators ===========
def login_required(req):
    def sessionDecorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            try:
                sessID = req.form['sessionID']
                if session.get('logged_in') and (sessID == session['sessionID']):
                    return f(*args, **kwargs)
                else:
                    return jsonify({
                        'code': 403,
                        'message': 'You are unauthorized to access that'
                        })
            except (KeyError, SyntaxError):
                    return jsonify({
                        'code': 400,
                        'message': 'SessionID is missing'
                        })
        return wrap
    return sessionDecorator

# ======================
# routes ===============
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# ================
# routes.api =====
@app.route('/api/logout')
@login_required(request)
def logout():
    session.pop('logged_in', None)
    session.pop('sessionID', None)
    return jsonify({
        'code': 205,
        'message': 'Sucessfully logged out'
        })

@app.route('/api/login', methods=['POST'])
def API_login():
    response = None
    if request.method == 'POST':
        try:
            email = ast.literal_eval(request.data.decode('UTF-8'))['email']
            password = ast.literal_eval(request.data.decode('UTF-8'))['password']
        except (ValueError, KeyError):
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
            session['email'] = str(email).split('@')[0]
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
        except (ValueError, KeyError):
            return jsonify({
                'code': 400,
                'message': 'Invalid input'
            })
        if len(email) < 3 or len(password) < 8:
            return jsonify({
                'code': 422,
                'message': 'Minimal length of password is 8, minimal length of email is 4'
            })
        q = db.session.query(User).filter_by(email=email).first()  # return None if nothing got selected
        if q:
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
        os.mkdir(os.path.join(UPLOAD_ROOT,str(email).split('@')[0]))
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

@app.route('/api/upload', methods=['POST'])
@login_required(request)
def API_upload():
    f = request.files['file']
    fname = secure_filename(f.filename)
    try:
        if allowed_file(fname,ALLOWED_EXTENSIONS):
            f.save(os.path.join(UPLOAD_ROOT,session['email'],fname))
        else:
            return jsonify({
                'code': 405,
                'message': 'Unsuported type of file'
                })
    except KeyError:
        return jsonify({
            'code': 400,
            'message': 'That user doesnt exists'
            })
    return jsonify({
        'code': 201,
        'message': 'Sucessfully uploaded file %s' % secure_filename(f.filename)
        })


@app.route('/api/download/<string:user>/<string:file>', methods=['POST'])
@login_required
def API_download():
    pass #Implement me


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
    os.mkdir(os.path.join(UPLOAD_ROOT,'test'))

if __name__ == '__main__':
    print("Please run main.py to start server")
    sys.exit(1)
