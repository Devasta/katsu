import unittest
import katsuserver
import katsuserver.blueprints.users.models


class AuthTests(unittest.TestCase):

    def setUp(self):
        self.App = katsuserver.create_app(config_name='testing')
        self.client = self.App.test_client()
        self.app_context = self.App.app_context()
        self.app_context.push()
        self.testuser = {
            'email': 'daniel@devasta.ie',
            'password': 'testpassword',
            'forename': 'Daniel',
            'surname': 'Murphy',
            'rolename': 'CU Member'
        }
        katsuserver.blueprints.users.models.create_user(
            email=self.testuser['email'],
            password=self.testuser['password'],
            forename=self.testuser['forename'],
            surname=self.testuser['surname'],
            rolename=self.testuser['rolename']
        )

    def tearDown(self):
        self.app_context.pop()
        self.App.db.delete_DB()

    def test_login(self):
        user = {
            'email': self.testuser['email'],
            'password': self.testuser['password']
        }
        response = self.client.post('/login/', json=user)
        self.assertEqual(response.status_code, 201)

    def test_login_GeraldWeinberg(self):
        user = {
            'email': self.testuser['email'],
            'password': 'W   M   JKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK'
        }
        response = self.client.post('/login/', json=user)
        self.assertEqual(response.status_code, 401)

    def test_incomplete_login(self):
        '''
        Submit username but no password
        :return:
        '''
        user = {
            'email': self.testuser['email']
        }
        response = self.client.post('/login/', json=user)
        self.assertEqual(response.status_code, 400)

    def test_incorrect_password(self):
        user = {
            'email': self.testuser['email'],
            'password': 'testwrongpassword'
        }
        response = self.client.post('/login/', json=user)
        self.assertEqual(response.status_code, 401)

    def test_invalid_login_data(self):
        user = {
            'email': 'daniel@devastaie',  # Invalid Email
            'password': 'testpassword'
        }
        response = self.client.post('/login/', json=user)
        self.assertEqual(response.status_code, 400)

    def test_loggedin_check_when_logged_in(self):
        user = {
            'email': self.testuser['email'],
            'password': self.testuser['password']
        }
        self.client.post('/login/', json=user)
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_loggedin_check_when_not_logged_in(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 401)

    def test_loggedin_check_when_cookies_cleared(self):
        user = {
            'email': self.testuser['email'],
            'password': self.testuser['password']
        }
        self.client.post('/login/', json=user)
        self.client.cookie_jar.clear()

        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        user = {
            'email': self.testuser['email'],
            'password': self.testuser['password']
        }
        self.client.post('/login/', json=user)
        response = self.client.delete('/login/')
        self.assertEqual(response.status_code, 204)

    def test_logout_when_not_logged_in(self):
        response = self.client.delete('/login/')
        self.assertEqual(response.status_code, 401)

    def test_CSRF(self):
        response = self.client.get('/CSRF/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()