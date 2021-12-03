import jsonschema


class SavingSearchSchema:

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
                },
                'status': {
                    'type': 'string',
                    'required': False,
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
            self.errors = [{error.path[0]: error.message} for error in sorted(v.iter_errors(self.data), key=str)]
            return False


class SavingsAccountSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'memberid': {
                    'type': 'integer',
                    'required': True
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