from application import db
from application.models import Users, Games, Market, UserGames

db.drop_all()
db.create_all()