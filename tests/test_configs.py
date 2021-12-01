import unittest
import flask
import katsuserver
import katsuserver.blueprints.users.models


class ConfigsTests(unittest.TestCase):

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

    def test_cant_get_configs_without_login(self):
        response = self.client.get('/configs/')
        self.assertEqual(response.status_code, 401)

    def test_cant_get_configs_without_permission(self):
        self.helper_loginasuser(rolename='CU Member')
        response = self.client.get('/configs/')
        self.assertEqual(response.status_code, 403)

    def test_can_get_configs(self):
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.get('/configs/')
        self.assertEqual(response.status_code, 200)

    def test_can_filter_configs(self):
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.get('/configs/?configname=CU_NAME')
        self.assertEqual(len(flask.json.loads(response.data)['configs']), 1)

    def test_cant_update_configs_without_login(self):
        config = {
                    'configname': 'CU_NAME',
                    'configvalue': 'CU NAME CHANGE',
                    'description': 'Some Description'
        }
        response = self.client.put('/configs/CU_NAME/', json=config)
        self.assertEqual(response.status_code, 401)

    def test_cant_update_configs_without_permission(self):
        config = {
                    'configname': 'CU_NAME',
                    'configvalue': 'CU NAME CHANGE',
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='CU Member')
        response = self.client.put('/configs/CU_NAME/', json=config)
        self.assertEqual(response.status_code, 403)

    def test_cant_update_configs_that_doesnt_exist(self):
        config = {
                    'configname': 'XXXXXXXXXX',
                    'configvalue': 'SOME CONFIG',
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/configs/XXXXXXXXXX/', json=config)
        self.assertEqual(response.status_code, 404)

    def test_cant_update_config_missing_data(self):
        config = {
            'configname': 'CU_NAME',
            'configvalue': 'NEW NAME'
            #'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/configs/CU_NAME/', json=config)
        self.assertEqual(response.status_code, 400)

    def test_cant_update_config_invalid_data(self):
        config = {
            'configname': 'CU_NAME',
            'configvalue': 'NEW NAME',
            'description': 'This is an excessively long description, too long for the database in fact.'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/configs/CU_NAME/', json=config)
        self.assertEqual(response.status_code, 400)

    def test_cant_update_config_invalid_URL(self):
        config = {
            'configname': 'NOT_CU_NAME',
            'configvalue': 'NEW NAME',
            'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/configs/CU_NAME/', json=config)
        self.assertEqual(response.status_code, 400)

    def test_can_update_config(self):
        config = {
                    'configname': 'CU_NAME',
                    'configvalue': 'NEW NAME',
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/configs/CU_NAME/', json=config)
        self.assertEqual(response.status_code, 204)

    def test_can_update_config_non_ASCII_chars(self):
        config = {
                    'configname': 'CU_NAME',
                    'configvalue': '労働金庫',
                    'description': 'ろうきん'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.put('/configs/CU_NAME/', json=config)
        self.assertEqual(response.status_code, 204)

    def test_cant_insert_configs_without_login(self):
        config = {
                    'configname': 'DEMO_CONFIG',
                    'configvalue': 'DEMO VALUE',
                    'description': 'Some Description'
        }
        response = self.client.post('/configs/', json=config)
        self.assertEqual(response.status_code, 401)

    def test_cant_insert_configs_without_permission(self):
        config = {
                    'configname': 'DEMO_CONFIG',
                    'configvalue': 'DEMO VALUE',
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='CU Member')
        response = self.client.post('/configs/', json=config)
        self.assertEqual(response.status_code, 403)

    def test_cant_insert_config_missing_data(self):
        config = {
            'configname': 'DEMO_CONFIG',
            'configvalue': 'DEMO VALUE'
            #'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.post('/configs/', json=config)
        self.assertEqual(response.status_code, 400)

    def test_cant_insert_config_invalid_data(self):
        config = {
            'configname': 'DEMO_CONFIG',
            'configvalue': 'DEMO VALUE',
            'description': 'This is an excessively long description, too long for the database in fact.'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.post('/configs/', json=config)
        self.assertEqual(response.status_code, 400)

    def test_can_insert_config(self):
        config = {
                    'configname': 'DEMO_CONFIG',
                    'configvalue': 'DEMO VALUE',
                    'description': 'Some Description'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.post('/configs/', json=config)
        self.assertEqual(response.status_code, 201)

    def test_can_insert_config_non_ASCII_chars(self):
        config = {
                    'configname': 'DEMO_CONFIG',
                    'configvalue': '労働金庫',
                    'description': 'ろうきん'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        response = self.client.post('/configs/', json=config)
        self.assertEqual(response.status_code, 201)

    def test_cant_insert_duplicate_configs(self):
        config = {
                    'configname': 'DEMO_CONFIG',
                    'configvalue': '労働金庫',
                    'description': 'ろうきん'
        }
        self.helper_loginasuser(rolename='Sysadmin')
        self.client.post('/configs/', json=config)
        response = self.client.post('/configs/', json=config)
        self.assertEqual(response.status_code, 409)

    def test_cant_delete_configs(self):
        '''
            If this test returns anything other than 405 not implemented, something disasterous has happened.
        '''
        response = self.client.delete('/configs/CU_NAME/')
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
