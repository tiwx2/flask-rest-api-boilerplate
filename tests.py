import unittest
from app.models import User
from app import create_app, db
from config import Config
import base64

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class InitialCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_trivial(self):
        self.assertTrue(True)

class UserCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = User(email="foo@bar.fr")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create(self):
        us = User.query.all()
        u = us[0]
        self.assertTrue(len(us) == 1)
        self.assertTrue(u.email == "foo@bar.fr")

    def test_create(self):
        us = User.query.all()
        u = us[0]
        self.assertTrue(len(us) == 1)
        self.assertTrue(u.email == "foo@bar.fr")

    def test_create_token(self):
        u = User.query.first()
        u.get_token()
        db.session.add(u)
        db.session.commit()
        self.assertTrue(len(u.token) == 32)

    def test_check_token(self):
        u = User.query.first()
        token = u.get_token()
        self.assertTrue(u.check_token(token))
        u.revoke_token()
        self.assertFalse(u.check_token(token))
        new_token = u.get_token()
        self.assertTrue(new_token != token)
        self.assertFalse(u.check_token(token))
        self.assertTrue(u.check_token(new_token))
        db.session.add(u)
        db.session.commit()

class PermissionsCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = User(email="foo@bar.fr")
        user.set_password('foobar')
        user.get_token()
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unprotected(self):
        with self.app.test_client() as c:
            response = c.get('/api/unprotected')
            self.assertEqual(response.status_code, 200)

    def test_basic_protected(self):
        u = User.query.first()
        username = u.email
        password = 'foobar'
        basic_headers = {
            'Authorization': 'Basic ' + base64.b64encode(bytes("{0}:{1}".format(username, password), 'utf-8')).decode('utf-8')
        }
        self.assertTrue(u is not None)
        self.assertTrue(u.check_password('foobar'))
        self.assertFalse(u.check_password('fooba'))
        with self.app.test_client() as c:
            response = c.get('/api/protected')
            self.assertEqual(response.status_code, 401)
            response = c.get('/api/protected', headers=basic_headers)
            self.assertEqual(response.status_code, 200)

    def test_token_protected(self):
        u = User.query.first()
        token = u.get_token()
        headers = {
            'Authorization': 'Bearer ' + token
        }

        username = u.email
        password = 'foobar'
        basic_headers = {
            'Authorization': 'Basic ' + base64.b64encode(bytes("{0}:{1}".format(username, password), 'utf-8')).decode('utf-8')
        }

        with self.app.test_client() as c:
            response = c.post('/api/token', headers=basic_headers)
            self.assertEqual(response.json['token'], token)
            response = c.get('/api/token-protected')
            self.assertEqual(response.status_code, 401)
            response = c.get('/api/token-protected', headers=headers)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main(verbosity=2)