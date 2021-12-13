import sys
import unittest
import traceback
import katsuserver.blueprints.users.models
import flask


class LoansTest(unittest.TestCase):

    def helper_loginasuser(self, rolename):
        try:
            katsuserver.blueprints.users.models.create_user(
                email=f'{rolename.replace(" ", "")}@devasta.ie',
                password='testpassword',
                forename='Daniel',
                surname='Murphy',
                rolename=rolename
            )
        except:
            pass
        self.client.post('/login/', json={
            'email': f'{rolename.replace(" ", "")}@devasta.ie',
            'password': 'testpassword'
        })

    def setUp(self):
        self.App = katsuserver.create_app(config_name='testing')
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
        
    def test_cant_get_loans_without_login(self):
        response = self.client.get('/loans/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_loan_without_login(self):
        response = self.client.get('/loans/1/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_loans_without_permission(self):
        self.helper_loginasuser('CU Member')
        response = self.client.get('/loans/')
        self.assertEqual(response.status_code, 403)

    def test_cant_get_loan_without_permission(self):
        self.helper_loginasuser('CU Member')
        response = self.client.get('/loans/1/')
        self.assertEqual(response.status_code, 403)

    def test_can_get_loans(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        self.client.post('/loans/', json=loandata)
        self.client.post('/loans/', json=loandata)
        self.client.post('/loans/', json=loandata)

        response = self.client.get('/loans/')
        self.assertEqual(len(flask.json.loads(response.data)['loans']), 3)

    def test_can_search_loans(self):
        self.helper_loginasuser('Member Services Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        self.client.post('/loans/', json=loandata)
        self.client.post('/loans/', json=loandata)
        self.client.post('/loans/', json=loandata)
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
        loandata = {
                    'memberid': memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        self.client.delete('/login/')
        self.helper_loginasuser('Loan Officer')
        self.client.post('/loans/', json=loandata)
        self.client.post('/loans/', json=loandata)

        response = self.client.get(f'/loans/?memberid={memberid}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(flask.json.loads(response.data)['loans']), 2)

        response = self.client.get(f'/loans/?memberid=99999999999')
        self.assertEqual(response.status_code, 204)

    def test_can_get_loan(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        response = self.client.get(f"/loans/{flask.json.loads(response.data)['loanid']}/")
        self.assertEqual(response.status_code, 200)

    def test_cant_get_loan_that_doesnt_exist(self):
        self.helper_loginasuser('Loan Officer')
        response = self.client.get('/loans/9999999/')
        self.assertEqual(response.status_code, 404)

    def test_cant_create_loan_without_login(self):
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        self.assertEqual(response.status_code, 401)

    def test_cant_create_loan_without_permission(self):
        self.helper_loginasuser('CU Member')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        self.assertEqual(response.status_code, 403)

    def test_can_create_loan(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        self.assertEqual(response.status_code, 201)

    def test_cant_create_incomplete_loan(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        self.assertEqual(response.status_code, 400)

    def test_cant_create_loan_invalid_member(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': 999999,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        self.assertEqual(response.status_code, 404)

    def test_cant_update_loan_without_permission(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)

        loanid = flask.json.loads(response.data)['loanid']
        self.client.delete('/login/')
        self.helper_loginasuser('CU Member')
        loandata['amount'] = 201
        response2 = self.client.patch(f"/loans/{loanid}/", json=loandata)
        self.assertEqual(response2.status_code, 403)

    def test_can_update_loan(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)

        loanid = flask.json.loads(response.data)['loanid']
        loandata2 = {
            'interestrate': 0.05,
            'paymentamount': 100,
            'paymentfrequency': 'M'
        }
        response2 = self.client.patch(f"/loans/{loanid}/", json=loandata2)
        self.assertEqual(response2.status_code, 204)

    def test_cant_update_loan_that_doesnt_exist(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.patch(f"/loans/99999999/", json=loandata)
        self.assertEqual(response.status_code, 404)

    def test_cant_close_loan_without_reason(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']
        response2 = self.client.patch(f"/loans/{loanid}/", json={
                                                               'statusid':'C'
                                                               })
        self.assertEqual(response2.status_code, 400)

    def test_can_close_loan(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']
        response2 = self.client.patch(f"/loans/{loanid}/", json={
                                                               'statusid':'C',
                                                               'closecode': 1
                                                               })
        print(response2.data)
        self.assertEqual(response2.status_code, 204)

    def test_cant_amend_closed_loan(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']
        self.client.patch(f"/loans/{loanid}/", json={
                                                               'statusid':'C',
                                                               'closecode': 1
                                                               })
        response2 = self.client.patch(f"/loans/{loanid}/", json={
                                                                'amount': 201
                                                                })
        self.assertEqual(response2.status_code, 400)

    def test_cant_amend_invalid_payment_amount(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']
        response2 = self.client.patch(f"/loans/{loanid}/", json={
                                                        'paymentamount': -1 # Can't be negative
                                                     })
        self.assertEqual(response2.status_code, 400)

    def test_cant_PUT_only_PATCH(self):
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)

        loanid = flask.json.loads(response.data)['loanid']
        loandata['amount'] = 201
        response2 = self.client.put(f"/loans/{loanid}/", json=loandata)
        self.assertEqual(response2.status_code, 405)

    def test_cant_delete_loan(self):
        '''
            If this test returns anything other than 405 not implemented, something disasterous has happened.
        '''
        response = self.client.delete('/loans/1/')
        self.assertEqual(response.status_code, 405)

    def test_approved_loan_transfers_money(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid,
                       'currency': 'EUR'}
        response = self.client.post('/savings/', json=accountdata)
        savingsaccount = flask.json.loads(response.data)['accountid']
        self.client.delete('/login/')

        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']
        response = self.client.patch(f'/loans/{loanid}/', json={
                                                    'interestrate': 2.5,
                                                    'paymentamount': 10,
                                                    'paymentmethodid': 'CA'
                                                     })
        response = self.client.patch(f'/loans/{loanid}/', json={'statusid': 'D'})
        response = self.client.patch(f'/loans/{loanid}/', json={
                                                                'statusid': 'A',
                                                                'savingsaccountid': savingsaccount
                                                                })
        self.assertEqual(response.status_code, 204)

    def test_cant_approve_loan_without_permission(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid,
                       'currency': 'EUR'}
        response = self.client.post('/savings/', json=accountdata)
        savingsaccount = flask.json.loads(response.data)['accountid']
        self.client.delete('/login/')

        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']
        self.client.delete('/login/')
        self.helper_loginasuser('Member Services Officer')
        response = self.client.patch(f'/loans/{loanid}/', json={'statusid': 'D'})

        self.assertEqual(response.status_code, 403)

    def test_cant_approve_loan_above_limit(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid,
                       'currency': 'EUR'}
        response = self.client.post('/savings/', json=accountdata)
        savingsaccount = flask.json.loads(response.data)['accountid']
        self.client.delete('/login/')

        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 1000000,
                    'currency': 'EUR',
                    'purpose': 'A very nice bicycle.'
                    }

        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']
        self.client.patch(f'/loans/{loanid}/', json={
                                                    'interestrate': 2.5,
                                                    'paymentamount': 100
                                                     })

        response = self.client.patch(f'/loans/{loanid}/', json={'statusid': 'D'})
        self.assertEqual(response.status_code, 403)

    def test_cant_approve_loan_missing_data(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid,
                       'currency': 'EUR'}
        self.client.delete('/login/')
        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle.'
                    }
        response = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(response.data)['loanid']

        response = self.client.patch(f'/loans/{loanid}/', json={'statusid': 'D'})
        self.assertEqual(response.status_code, 400)

    def test_cant_close_loan_with_money_still_owed(self):
        self.helper_loginasuser('Member Services Officer')
        accountdata = {'memberid': self.memberid,
                       'currency': 'EUR'}
        a = self.client.post('/savings/', json=accountdata)
        savingsaccount = flask.json.loads(a.data)['accountid']
        self.client.delete('/login/')

        self.helper_loginasuser('Loan Officer')
        loandata = {
                    'memberid': self.memberid,
                    'amount': 200,
                    'currency': 'EUR',
                    'purpose': 'Bicycle'
                    }
        l = self.client.post('/loans/', json=loandata)
        loanid = flask.json.loads(l.data)['loanid']
        self.client.patch(f'/loans/{loanid}/', json={
                                                    'interestrate': 2.5,
                                                    'paymentamount': 10,
                                                    'paymentmethodid': 'CA'
                                                     })
        self.client.patch(f'/loans/{loanid}/', json={'statusid': 'D'})
        self.client.patch(f'/loans/{loanid}/', json={
                                                                'statusid': 'A',
                                                                'savingsaccountid': savingsaccount
                                                                })
        q = self.client.get(f'/loans/{loanid}/')
        response = self.client.patch(f'/loans/{loanid}/', json={'statusid': 'C',
                                                     'closecode': 1})
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
