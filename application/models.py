from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return ''.join(['UserID: ', str(self.id), '\r\n', 'Email: ', self.email])

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    market = db.relationship('Market', backref = 'gameMarket', lazy = True)
    usergames = db.relationship('UserGames', backref = 'userGames', lazy = True)

    def __repr__(self):
        return ''.join(['GameID: ', str(self.id), '\r\n', 'Game Name: ', self.game_name])

class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer, db.ForeignKey('games.id'), nullable = False)
    seller = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float(7,2), nullable = False)

    def __repr__(self):
        return ''.join(['ID : ' , str(self.id), '\r\n', 'Game : ' , str(self.game)])

class UserGames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer, db.ForeignKey('games.id'), nullable = False)
    user = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return ''.join(['ID : ', str(self.id), '\r\n', 'Game : ', str(self.game), '\r\n', 'User'])