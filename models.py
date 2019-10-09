from server import db


class User(db.Model):
    '''
        IDUser(PK autoincrement)
        email[string]
        password[string]
        validated[int]
    '''
    IDUser = db.Column('IDUser', db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    validated = db.Column(db.Boolean, nullable=False)
    dotfiles = db.relationship('dotfile', backref='user', lazy=True)

    def __repr__(self):
        return self.email


class Dotfile(db.Model):
    '''
        IDDotfile[PK autoincrement]
        createdOn[DateTime]
        password[string]
        user_id[FK IDUser]
    '''
    IDDotfile = db.Column('IDDotfile', db.Integer, primary_key=True)
    createdOn = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.IDUser'),
                        nullable=False)
