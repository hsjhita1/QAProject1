import unittest

from flask import url_for
from flask_testing import TestCase

from application import app, db, bcrypt
from application.models import Users, Games, Market, UserGames
from os import getenv

class TestBase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI = getenv('FLASK_DB_URI'),
            SECRET_KEY = getenv('FLASK_SECRET_KEY'),
            WTF_CSRF_ENABLED = False,
            DEBUG = True
        )
        return app

    def setUp(self):
        # Delete data in the database
        db.session.commit()
        db.drop_all()
        db.create_all()

        #Create user 1
        hashed_pw_1 = bcrypt.generate_password_hash('admin2020')
        admin = Users(
            user_name = "admin",
            first_name = "admin",
            last_name = "admin",
            email = "admin@test.com",
            password = hashed_pw_1
            )

        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_homepage_view(self):
        # Check if home is accessible without login
        homeResponse = self.client.get(url_for('home'))
        self.assertEqual(homeResponse.status_code, 200)

        # Check if games is accessible without login
        gameResponse = self.client.get(url_for('games'))
        self.assertEqual(gameResponse.status_code, 200)
