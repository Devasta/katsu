import jsonschema


class SavingSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'accountid': {
                    'type': 'integer'
                },
                'memberid': {
                    'type': 'string',
                    'pattern': r'''[0-9]'''
                },
                'status': {
                    'type': 'string',
                    'maxLength': 1
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
            self.errors = [error.message for error in sorted(v.iter_errors(self.data), key=str)]
            return False


class SavingsAccountSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'memberid': {
                    'type': 'integer'
                },
                'currency': {
                    'type': 'string',
                    'minimum': 3,
                    'maximum': 3
                }
            },
            'required': ['memberid', 'currency']
        }
        self.data = data
        self.errors = []

    def validate(self):
        self.errors = []
        v = jsonschema.Draft202012Validator(self.schema)

        if v.is_valid(self.data):
            return True
        else:
            self.errors = [error.message for error in sorted(v.iter_errors(self.data), key=str)]
            return False