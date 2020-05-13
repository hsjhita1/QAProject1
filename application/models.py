from application import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return ''.join([
            'User: ', self.first_name, ' ', self.last_name, '\r\n',
            'Title: ', self.title, '\r\n', 'Game: ', self.game, '\r\n', self.content
            ])

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
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return ''.join(['GameID: ', str(self.id), '\r\n', 'Game Name: ', self.game_name])