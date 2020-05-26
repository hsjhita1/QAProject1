import unittest
from blinker import Namespace
from flask import url_for, template_rendered
from flask_testing import TestCase
from application import app, db, bcrypt
from application.models import Users, Games, Market, UserGames
from os import getenv
from contextlib import contextmanager

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

        db.session.add(admin)
        db.session.commit()

    # Removes all data from the tables after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_home_page_view(self):
        # Check if home is accessible without login
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_games_page_view(self):
        # Check if games is accessible without login
        response = self.client.get(url_for('games'))
        self.assertEqual(response.status_code, 200)

    def test_market_page_view(self):
        # Check if market is accessible without login
        response = self.client.get(url_for('market'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_view(self):
        # Check if login is accessible without login
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_view(self):
        # Check if register is accessible without login
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_one_game_page_view(self):
        # Check if a single game is accessible without login
        game = Games(game_name = 'Test Game', description = 'Test Description')
        db.session.add(game)
        db.session.commit()
        name = game.game_name
        response = self.client.get(url_for('gameName', name = name))
        self.assertEqual(response.status_code, 200)

    def test_accountpage_view(self):
        # Check if account page is inaccessible without login
        targetPage = url_for('account', id = 1)
        redirectPage = url_for('login', next = targetPage)
        response = self.client.get(targetPage)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirectPage)

    def test_logout_view(self):
        # Check if logout page is inaccessible without login
        targetPage = url_for('logout', id = 1)
        redirectPage = url_for('login', next = targetPage)
        response = self.client.get(targetPage)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirectPage)

    def test_games_add_redirect(self):
        # Check if adding a game redirects to the game page
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for('addgame'),
                data = dict(
                    game = "Test Game",
                    description = "Test description"
                ),
                follow_redirects = True
            )
            self.assertIn(b'Test Game', response.data)

    def test_collection_game_add(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('addgame'),
                data = dict(
                    game = "Test Game",
                    description = "Test description"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for('add_collection'),
                data = dict(
                    game = 1
                ),
                follow_redirects = True
            )
            self.assertIn(b'1', response.data)


    def test_register_account(self):
        # Checks is an account can be registered
        with self.client:
            self.client.post(
                url_for('register'),
                data = dict(
                    user_name = "testuser",
                    first_name = "test",
                    last_name = "test",
                    email = "user@test.com",
                    password = "testuser",
                    confirm_password = "testuser"
                ),
                follow_redirects = True
            )
            self.assertEqual(Users.query.count(), 2)

    def test_update_game_post(self):
        # Checks to see if a game can update
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('addgame'),
                data = dict(
                    game = 'Test Game',
                    description = "Test description"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for('updateGame', name = 'Test Game'),
                data = dict(
                    game = 'Updated Game',
                    description = 'Updated Description'
                ),
                follow_redirects = True
            )
            self.assertIn(b'Updated Game', response.data)

            response2 = self.client.get(
                url_for('updateGame', name = 'Updated Game'),
            )
            self.assertIn(b'Updated Game', response2.data)

    def test_update_account(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for('account'),
                data = dict(
                    email = "admin@admin.com",
                    first_name = "administrator",
                    last_name = "administrator"
                ),
                follow_redirects = True
            )
            self.assertIn(b'admin@admin.com', response.data)

    def test_sell_game(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('addgame'),
                data = dict(
                    game = 'Test Game',
                    description = "Test description"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for('sellgame'),
                data = dict(
                    game = 1, # Game ID 1 being Test Game
                    description = 'Used',
                    price = 24.99,
                    seller = 'admin'
                ),
                follow_redirects = True
            )
            self.assertEqual(Market.query.count(), 1)

    def test_account_delete(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('addgame'),
                data = dict(
                    game = "Test Game",
                    description = "Test description"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('add_collection'),
                data = dict(
                    game = 1
                ),
                follow_redirects = True
            )
            redirectPage = url_for('account_delete')
            response = self.client.get(redirectPage)
            self.assertEqual(Users.query.count(), 0)

    def test_delete_game(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('addgame'),
                data = dict(
                    game = "Test Game",
                    description = "Test description"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('add_collection'),
                data = dict(
                    game = 1
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('sellgame'),
                data = dict(
                    game = 1, # Game ID 1 being Test Game
                    description = 'Used',
                    price = 24.99,
                    seller = 'admin'
                ),
                follow_redirects = True
            )
            redirectPage = url_for('gameDelete', name = 'Test Game')
            response = self.client.get(redirectPage)
            self.assertEqual(Games.query.count(), 0)

    def test_delete_game_collection(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('addgame'),
                data = dict(
                    game = "Test Game",
                    description = "Test description"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('add_collection'),
                data = dict(
                    game = 1
                ),
                follow_redirects = True
            )
            redirectPage = url_for('del_collection', name = 1)
            response = self.client.get(redirectPage)
            self.assertEqual(UserGames.query.count(), 0)

    def test_user_logged_register(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            targetPage = url_for('home')
            redirectPage = url_for('register')
            response = self.client.get(redirectPage)
            self.assertRedirects(response, targetPage)

    def test_user_logged_login(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            targetPage = url_for('home')
            redirectPage = url_for('login')
            response = self.client.get(redirectPage)
            self.assertRedirects(response, targetPage)

    def test_log_out(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            targetPage = url_for('login')
            redirectPage = url_for('logout')
            response = self.client.get(redirectPage)
            self.assertRedirects(response, targetPage)

    def test_no_game_col(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for('add_collection'),
                data = dict(
                    game = 1,
                    user = 'admin'
                )
            )
            targetPage = url_for('addgame')
            self.assertRedirects(response, targetPage)

    def test_duplicate_game(self):
        with self.client:
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "admin@test.com",
                    password = "admin2020"
                ),
                follow_redirects = True
            )
            self.client.post(
                url_for('addgame'),
                data = dict(
                    game = "Test Game",
                    description = "Test description"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for('addgame'),
                data = dict(
                    game = "Test Game",
                    description = "Test description"
                ),
                follow_redirects = True
            )
            self.assertEqual(Games.query.count(), 1)

class TestNotRenderTemplate(TestCase):

    render_templates = False

    def create_app(self):
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI = getenv('TEST_FLASK_DB_URI'),
            SECRET_KEY = getenv('TEST_FLASK_SECRET_KEY'),
            WTF_CSRF_ENABLED = False,
            DEBUG = True
        )
        return app
    
    def test_home(self):
        response = self.client.get('/')
        self.assert_template_used('home.html')