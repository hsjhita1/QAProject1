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
            SQLALCHEMY_DATABASE_URI = getenv('TEST_FLASK_DB_URI'),
            SECRET_KEY = getenv('TEST_FLASK_SECRET_KEY'),
            WTF_CSRF_ENABLED = False,
            DEBUG = True
        )
        return app

    def setUp(self):
        # Delete data in the database
        db.session.commit()
        db.drop_all()
        db.create_all()

        # Create user 1
        hashed_pw_1 = bcrypt.generate_password_hash('admin2020')
        admin = Users(
            user_name = "admin",
            first_name = "admin",
            last_name = "admin",
            email = "admin@test.com",
            password = hashed_pw_1
            )

        # Create user 2
        hashed_pw_2 = bcrypt.generate_password_hash('test2020')
        test = Users(
            user_name = "test",
            first_name = "test",
            last_name = "test",
            email = "test@test.com",
            password = hashed_pw_2
        )

        db.session.add(admin)
        db.session.add(test)
        db.session.commit()

    # Removes all data from the tables after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_homepage_view(self):
        # Check if home is accessible without login
        homeResponse = self.client.get(url_for('home'))
        self.assertEqual(homeResponse.status_code, 200)

    def test_gamespage_view(self):
        # Check if games is accessible without login
        gameResponse = self.client.get(url_for('games'))
        self.assertEqual(gameResponse.status_code, 200)

    def test_accountpage_view(self):
        # Check if account page is inaccessible without login
        targetPage = url_for('account', id = 1)
        redirectPage = url_for('login', next = targetPage)
        accountResponse = self.client.get(targetPage)
        self.assertEqual(accountResponse.status_code, 302)
        self.assertRedirects(accountResponse, redirectPage)

    def test_logout_view(self):
        # Check if logout page is inaccessible without login
        targetPage = url_for('logout', id = 1)
        redirectPage = url_for('login', next = targetPage)
        logoutResponse = self.client.get(targetPage)
        self.assertEqual(logoutResponse.status_code, 302)
        self.assertRedirects(logoutResponse, redirectPage)

    def test_games_add_model(self):
        # Test to see if data is being inserted into games
        game = Games(game_name = 'Test Game', description = 'Test Description')
        db.session.add(game)
        db.session.commit()
        self.assertEqual(Games.query.count(), 1)

    def test_games_delete_model(self):
        # Check if data is being deleted from the database
        game = Games(game_name = 'Test Game', description = 'Test Description')
        game2 = Games(game_name = 'Test Game 2', description = 'Test Description')
        db.session.add(game)
        db.session.add(game2)
        db.session.commit()
        db.session.delete(game)
        db.session.commit()
        self.assertEqual(Games.query.count(), 1)