import jsonschema


'''
TODO SORT FILE UPLOADS

class DocumentUploadSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'accountid': {
                    'type': 'integer',
                    'required': True
                },
                'document': {
                    'type': 'string', # What should this be???
                    'required': True
                },
                'description': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 50
                }
            }
        }
        self.data = data
        self.errors = []

    def validate(self):
        self.errors = []
        v = jsonschema.Draft202012Validator(self.schema)

        if v.is_valid(self.data):
            return True
        else:
            self.errors = [{error.path[0]: error.message} for error in sorted(v.iter_errors(self.data), key=str)]
            return False
'''


class ConfigSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'accountid': {
                    'type': 'integer',
                    'required': False
                },
                'memberid': {
                    'type': 'integer',
                    'required': False
                }
            }
        }
        self.data = data
        self.errors = []

    def validate(self):
        self.errors = []
        v = jsonschema.Draft202012Validator(self.schema)

        if v.is_valid(self.data):
            return True
        else:
            self.errors = [{error.path[0]: error.message} for error in sorted(v.iter_errors(self.data), key=str)]
            return False
