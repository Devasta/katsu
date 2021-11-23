import unittest
import app.blueprints.users.models
import flask


class SavingsTests(unittest.TestCase):

    def helper_loginasuser(self, rolename):
        app.blueprints.users.models.create_user(
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
        self.App = app.create_app(config_name='testing')
        self.client = self.App.test_client()
        self.app_context = self.App.app_context()
        self.app_context.push()

        member = {
            'title': 'Mr',
            'forename': 'Daniel',
            'surname': 'Murphy',
            'addressline1': '1234 Test Street',
            'addressline2': 'Test Town',
            'city': 'Cork City',
            'county': 'Cork',
            'country': 'Ireland',
            'postcode': 'XXX XXXX'
        }
        self.helper_loginasuser('Manager')
        response = self.client.post('/members/', json=member)
        self.memberid = flask.json.loads(response.data)['memberid']
        self.client.delete('/login/')

    def tearDown(self):
        self.App.db.delete_DB()
        self.app_context.pop()

    def test_cant_get_savingsaccounts_without_login(self):
        response = self.client.get('/savings/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_savingsaccount_without_login(self):
        response = self.client.get('/savings/1/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_savingsaccounts_without_permission(self):
        self.helper_loginasuser('CU Member')
        response = self.client.get('/savings/')
        self.assertEqual(response.status_code, 403)

    def test_cant_get_savingsaccount_without_permission(self):
        self.helper_loginasuser('CU Member')
        response = self.client.get('/savings/1/')
        self.assertEqual(response.status_code, 403)

    def test_can_get_savingsaccounts(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid}
        self.client.post('/savings/', json=accountdata)
        self.client.post('/savings/', json=accountdata)
        self.client.post('/savings/', json=accountdata)

        response = self.client.get('/savings/')
        self.assertEqual(len(flask.json.loads(response.data)['savingsaccounts']), 3)

    def test_can_search_savingsaccounts(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid}
        self.client.post('/savings/', json=accountdata)
        self.client.post('/savings/', json=accountdata)
        self.client.post('/savings/', json=accountdata)
        member = {
            'title': 'Mr',
            'forename': 'Daniel',
            'surname': 'Murphy',
            'addressline1': '1234 Test Street',
            'addressline2': 'Test Town',
            'city': 'Cork City',
            'county': 'Cork',
            'country': 'Ireland',
            'postcode': 'XXX XXXX'
        }
        response = self.client.post('/members/', json=member)
        memberid = flask.json.loads(response.data)['memberid']
        accountdata = {'memberid': memberid}
        self.client.post('/savings/', json=accountdata)
        self.client.post('/savings/', json=accountdata)

        response = self.client.get(f'/savings/?memberid={memberid}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(flask.json.loads(response.data)['savingsaccounts']), 2)

        response = self.client.get(f'/savings/?memberid=99999999999')
        self.assertEqual(response.status_code, 204)

    def test_can_get_savingsaccount(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid}
        response = self.client.post('/savings/', json=accountdata)

        response = self.client.get(f"/savings/{flask.json.loads(response.data)['accountid']}/")
        self.assertEqual(response.status_code, 200)

    def test_cant_get_savingsaccount_that_doesnt_exist(self):
        self.helper_loginasuser('Member Services Officer')
        response = self.client.get('/savings/9999999/')
        self.assertEqual(response.status_code, 404)

    def test_cant_create_savingsaccount_without_login(self):
        accountdata = {'memberid': self.memberid}
        response = self.client.post('/savings/', json=accountdata)
        self.assertEqual(response.status_code, 401)

    def test_cant_create_savingsaccount_without_permission(self):
        self.helper_loginasuser('CU Member')
        accountdata = {'memberid': self.memberid}
        response = self.client.post('/savings/', json=accountdata)
        self.assertEqual(response.status_code, 403)

    def test_can_create_savingsaccount(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid}
        response = self.client.post('/savings/', json=accountdata)
        self.assertEqual(response.status_code, 201)

    def test_cant_create_incomplete_savingsaccount(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {}
        response = self.client.post('/savings/', json=accountdata)
        self.assertEqual(response.status_code, 400)

    def test_cant_create_savingsaccount_invalid_member(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': 999999}  # Member that doesn't exist
        response = self.client.post('/savings/', json=accountdata)
        self.assertEqual(response.status_code, 404)

    def test_cant_delete_savingsaccount(self):
        '''
            If this test returns anything other than 405 not implemented, something disasterous has happened.
        '''
        response = self.client.delete('/savings/1/')
        self.assertEqual(response.status_code, 405)
