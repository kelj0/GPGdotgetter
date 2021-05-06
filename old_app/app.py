from flask import Flask


app = Flask('savedots')
app.config['DATABASE_FILE'] = 'savedots_DB.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///savedots_DB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "CHANGE_ME"

if __name__ == '__main__':
    print("Please run main.py to start server")
    exit(1)
