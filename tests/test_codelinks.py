import unittest
import flask
import katsuserver
import katsuserver.blueprints.users.models


class codelinksTests(unittest.TestCase):

    def helper_loginasuser(self, rolename):
        katsuserver.blueprints.users.models.create_user(
            email=f'{rolename.replace(" ","")}@devasta.ie',
            password='testpassword',
            forename='Daniel',
            surname='Murphy',
            rolename=rolename
        )
        self.client.post('/login/', json={
            'email': f'{rolename.replace(" ","")}@devasta.ie',
            'password': 'testpassword'
        })

    def setUp(self):
        self.App = katsuserver.create_app(config_name='testing')
        self.client = self.App.test_client()
        self.app_context = self.App.app_context()
        self.app_context.push()

    def tearDown(self):
        self.App.db.delete_DB()

    def test_cant_get_codelinks_without_login(self):
        response = self.client.get('/codelinks/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_codelinks_without_permission(self):
        self.helper_loginasuser(rolename='CU Member')
        response = self.client.get('/codelinks/')
        self.assertEqual(response.status_code, 403)

    def test_can_get_codelinks(self):
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.get('/codelinks/')
        self.assertEqual(response.status_code, 200)

    def test_can_filter_codelinks(self):
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.get('/codelinks/?codelinkname=CASH_ACCOUNT')
        self.assertEqual(len(flask.json.loads(response.data)['codelinks']), 1)

    def test_cant_update_codelinks_without_login(self):
        codelink = {
                    'codelinkname': 'CASH_ACCOUNT',
                    'accountid': 1,
                    'description': 'Some Description'
        }
        response = self.client.put('/codelinks/CASH_ACCOUNT/', json=codelink)
        self.assertEqual(response.status_code, 401)

    def test_cant_update_codelinks_without_permission(self):
        codelink = {
                    'codelinkname': 'CASH_ACCOUNT',
                    'accountid': 1,
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='CU Member')
        response = self.client.put('/codelinks/CASH_ACCOUNT/', json=codelink)
        self.assertEqual(response.status_code, 403)

    def test_cant_update_codelinks_that_doesnt_exist(self):
        codelink = {
                    'codelinkname': 'XXXXXXXXXX',
                    'accountid': 1,
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/codelinks/XXXXXXXXXX/', json=codelink)
        self.assertEqual(response.status_code, 404)

    def test_cant_update_codelink_missing_data(self):
        codelink = {
            'codelinkname': 'CASH_ACCOUNT',
            'accountid': 1
            #'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/codelinks/CASH_ACCOUNT/', json=codelink)
        self.assertEqual(response.status_code, 400)

    def test_cant_update_codelink_invalid_data(self):
        codelink = {
            'codelinkname': 'CASH_ACCOUNT',
            'accountid': 'NEW NAME',
            'description': 'This is an excessively long description, too long for the database in fact.'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/codelinks/CASH_ACCOUNT/', json=codelink)
        self.assertEqual(response.status_code, 400)

    def test_cant_update_codelink_invalid_URL(self):
        codelink = {
            'codelinkname': 'NOT_CASH_ACCOUNT',
            'accountid': 1,
            'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/codelinks/CASH_ACCOUNT/', json=codelink)
        self.assertEqual(response.status_code, 400)

    def test_can_update_codelink(self):
        codelink = {
                    'codelinkname': 'CASH_ACCOUNT',
                    'accountid': 1,
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/codelinks/CASH_ACCOUNT/', json=codelink)
        self.assertEqual(response.status_code, 204)


    def test_cant_insert_codelinks_without_login(self):
        codelink = {
                    'codelinkname': 'DEMO_CODELINK',
                    'accountid': 1,
                    'description': 'Some Description'
        }
        response = self.client.post('/codelinks/', json=codelink)
        self.assertEqual(response.status_code, 401)

    def test_cant_insert_codelinks_without_permission(self):
        codelink = {
                    'codelinkname': 'DEMO_CODELINK',
                    'accountid': 1,
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='CU Member')
        response = self.client.post('/codelinks/', json=codelink)
        self.assertEqual(response.status_code, 403)

    def test_cant_insert_codelink_missing_data(self):
        codelink = {
            'codelinkname': 'DEMO_CODELINK',
            'accountid': 1
            #'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.post('/codelinks/', json=codelink)
        self.assertEqual(response.status_code, 400)

    def test_cant_insert_codelink_invalid_data(self):
        codelink = {
            'codelinkname': 'DEMO_CODELINK',
            'accountid': 1,
            'description': 'This is an excessively long description, too long for the database in fact.'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.post('/codelinks/', json=codelink)
        self.assertEqual(response.status_code, 400)

    def test_can_insert_codelink(self):
        codelink = {
                    'codelinkname': 'DEMO_CODELINK',
                    'accountid': 1,
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.post('/codelinks/', json=codelink)
        self.assertEqual(response.status_code, 201)

    def test_cant_insert_duplicate_codelinks(self):
        codelink = {
                    'codelinkname': 'DEMO_CODELINK',
                    'accountid': 1,
                    'description': 'ろうきん'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        self.client.post('/codelinks/', json=codelink)
        response = self.client.post('/codelinks/', json=codelink)
        self.assertEqual(response.status_code, 409)

    def test_cant_delete_codelinks(self):
        '''
            If this test returns anything other than 405 not implemented, something disasterous has happened.
        '''
        response = self.client.delete('/codelinks/CASH_ACCOUNT/')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()