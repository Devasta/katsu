import unittest
import app.blueprints.users.models
import flask


class MyTestCase(unittest.TestCase):

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
        response = self.client.post('/savings/', json={'memberid': self.memberid})
        self.accountid = flask.json.loads(response.data)['accountid']
        self.client.delete('/login/')

    def cant_get_comments_without_login(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.data, 401)

    def cant_get_comments_without_permission(self):
        self.helper_loginasuser('CU Member')
        response = self.client.get('/comments/')
        self.assertEqual(response.data, 401)

    def can_get_comments(self):
        self.helper_loginasuser('Member Services Officer')
        comment = {'accountid': self.accountid, 'comment': 'testcomment'}
        self.client.post('/comments/', json=comment)
        response = self.client.get('/comments/')
        self.assertEqual(response.data, 200)

    def can_filter_comments(self):
        self.helper_loginasuser('Member Services Officer')

        self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'testcomment'})
        self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'testcomment'})
        self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'testcomment'})

        response = self.client.post('/savings/', json={'memberid': self.memberid})
        accountid = flask.json.loads(response.data)['accountid']

        self.client.post('/comments/', json={'accountid': accountid, 'comment': 'testcomment'})
        self.client.post('/comments/', json={'accountid': accountid, 'comment': 'testcomment'})
        self.client.post('/comments/', json={'accountid': accountid, 'comment': 'testcomment'})

        response = self.client.get(f'/comments/?accountid={accountid}')
        self.assertEqual(len(flask.json.loads(response.data)), 3)

        response = self.client.get(f'/comments/?accountid=99999999')
        self.assertEqual(response.status_code, 204)

    def can_paginate_comments(self):
        self.helper_loginasuser('Member Services Officer')

        for i in range(0, 7):
            self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'testcomment'})

        response = self.client.get('/comments/?page=1&limit=5')
        self.assertEqual(len(flask.json.loads(response.data)['comments']), 5)

        response = self.client.get('/comments/?page=2&limit=5')
        self.assertEqual(len(flask.json.loads(response.data)['comments']), 2)

    def cant_create_comment_without_login(self):
        response = self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'testcomment'})
        self.assertEqual(response.data, 401)

    def cant_create_comment_without_permission(self):
        self.helper_loginasuser('Sysadmin')
        response = self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'testcomment'})
        self.assertEqual(response.data, 403)

    def can_create_comment(self):
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'testcomment'})
        self.assertEqual(response.data, 201)

    def can_create_non_ASCII_comment(self):
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/comments/', json={'accountid': self.accountid, 'comment': 'Пролетарии всех стран, соединяйтесь!\nТебе нечего терять, кроме цепей!'})
        self.assertEqual(response.data, 201)

    def cant_create_comment_invalid_data(self):
        self.helper_loginasuser('Member Services Officer')
        comment = {'accountid': self.accountid}  # No comment!
        response = self.client.post('/comments/', json=comment)
        self.assertEqual(response.data, 201)

    def cant_create_comment_invalid_account(self):
        self.helper_loginasuser('Member Services Officer')
        response = self.client.post('/comments/', json={'accountid': 99999, 'comment': 'testcomment'})
        self.assertEqual(response.data, 404)

    def cant_update_comment(self):
        self.helper_loginasuser('Member Services Officer')
        response = self.client.put('/comments/1/', json={'accountid': 1, 'comment': 'testcomment2'})
        self.assertEqual(response.data, 405)

    def cant_delete_comment(self):
        self.helper_loginasuser('Member Services Officer')
        response = self.client.delete(f'/comments/1/')
        self.assertEqual(response.data, 405)

if __name__ == '__main__':
    unittest.main()