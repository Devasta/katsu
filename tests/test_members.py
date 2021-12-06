import unittest
import katsuserver
import katsuserver.blueprints.users.models
import flask


class MemberTests(unittest.TestCase):

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

    def test_cant_get_members_without_login(self):
        response = self.client.get('/members/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_member_without_login(self):
        response = self.client.get('/members/1/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_members_without_permission(self):
        self.helper_loginasuser('Sysadmin')
        response = self.client.get('/members/')
        self.assertEqual(response.status_code, 403)

    def test_cant_get_member_without_permission(self):
        self.helper_loginasuser('Sysadmin')
        response = self.client.get('/members/1/')
        self.assertEqual(response.status_code, 403)

    def test_can_get_members(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.get('/members/')
        self.assertEqual(response.status_code, 204)

        self.client.post('/members/', json=member)
        self.client.post('/members/', json=member)
        self.client.post('/members/', json=member)
        self.client.post('/members/', json=member)
        self.client.post('/members/', json=member)
        response = self.client.get('/members/')
        self.assertEqual(len(flask.json.loads(response.data)['members']), 5)

    def test_can_search_members(self):
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
        member2 = {
                    'forename': 'としこ',
                    'surname': 'こしじま',
                    'addressline1': '2 - chōme',
                    'addressline2': '3 Nagatachō',
                    'city': 'Chiyoda City',
                    'county': 'Tōkyō',
                    'country': 'Japan',
                    'postcode': 'XXX XXXX'
                  }
        self.helper_loginasuser('Member Services Officer')

        self.client.post('/members/', json=member)
        self.client.post('/members/', json=member2)

        response = self.client.get('/members/?surname=Murphy')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(flask.json.loads(response.data)), 1)

        response = self.client.get('/members/?surname=XXXMurphy')
        self.assertEqual(response.status_code, 204)

    def test_can_get_member(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)

        response = self.client.get(f"/members/{flask.json.loads(response.data)['memberid']}/")
        self.assertEqual(response.status_code, 200)

    def test_cant_get_member_that_doesnt_exist(self):
        self.helper_loginasuser('Member Services Officer')
        response = self.client.get('/members/9999999/')
        self.assertEqual(response.status_code, 404)

    def test_cant_create_member_without_login(self):
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
        self.assertEqual(response.status_code, 401)

    def test_cant_create_member_without_permission(self):
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
        self.helper_loginasuser('CU Member')
        response = self.client.post('/members/', json=member)
        self.assertEqual(response.status_code, 403)

    def test_can_create_member(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)
        self.assertEqual(response.status_code, 201)

    def test_can_create_non_ASCII_member(self):
        member = {
                    'forename': 'としこ',
                    'surname': 'こしじま',
                    'addressline1': '2 - chōme',
                    'addressline2': '3 Nagatachō',
                    'city': 'Chiyoda City',
                    'county': 'Tōkyō',
                    'country': 'Japan',
                    'postcode': 'XXX XXXX'
                  }
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)
        self.assertEqual(response.status_code, 201)

    def test_cant_create_incomplete_member(self):
        member = {
                    'title': 'Mr',
                    'forename': 'Daniel',
                    'surname': 'Murphy',
                    'addressline1': '1234 Test Street',
                    'addressline2': 'Test Town',
                    'city': 'Cork City',
                    'county': 'Cork',
                    'country': 'Ireland'
                    # No Postcode!
                  }
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)
        self.assertEqual(response.status_code, 400)

    def test_cant_create_invalid_member(self):
        member = {
                    'title': 'Mr',
                    'forename': 'Daniel',
                    'surname': 'Murphy',
                    'addressline1': '1234 Test Street',
                    'addressline2': 'Test Town',
                    'city': 'Cork City',
                    'county': 'Cork',
                    'country': 'Ireland'
                    'postcode' 'XXX XXXXXXXXXX'  # Invalid Postcode
                  }
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)
        self.assertEqual(response.status_code, 400)

    def test_cant_update_member_without_login(self):
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
        response = self.client.put('/members/1/', json=member)
        self.assertEqual(response.status_code, 401)

    def test_can_update_member(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)
        memberid = flask.json.loads(response.data)['memberid']
        member['postcode'] = 'YYY YYYY'
        response2 = self.client.put(f"/members/{memberid}/", json=member)
        self.assertEqual(response2.status_code, 204)

    def test_cant_update_member_invalid_data(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)
        memberid = flask.json.loads(response.data)['memberid']
        member['postcode'] = 'YYY YYYYYYYYYY'
        response2 = self.client.put(f"/members/{memberid}/", json=member)
        self.assertEqual(response2.status_code, 400)

    def test_cant_update_member_missing_data(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)
        memberid = flask.json.loads(response.data)['memberid']
        member.pop('postcode', None)
        response2 = self.client.put(f"/members/{memberid}/", json=member)
        self.assertEqual(response2.status_code, 400)

    def test_cant_update_member_without_permission(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/members/', json=member)

        memberid = flask.json.loads(response.data)['memberid']
        self.client.delete('/login/')
        self.helper_loginasuser('CU Member')
        member['postcode'] = 'YYY YYYY'
        response2 = self.client.put(f"/members/{memberid}/", json=member)
        self.assertEqual(response2.status_code, 403)

    def test_cant_update_member_that_doesnt_exist(self):
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
        self.helper_loginasuser('Member Services Officer')
        response = self.client.put('/members/9999999/', json=member)
        self.assertEqual(response.status_code, 404)

    def test_cant_delete_member(self):
        '''
            If this test returns anything other than 405 not implemented, something disasterous has happened.
        '''
        response = self.client.delete('/members/1/')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()