from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=getenv('FLASK_DB_URI')
app.config['SECRET_KEY'] = getenv('FLASK_SECRET_KEY')

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

from application import routes