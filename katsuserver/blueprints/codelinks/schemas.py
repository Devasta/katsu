import jsonschema


class CodelinkSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'codelinkname': {
                    'type': 'string',
                    'maxLength': 20
                },
                'accountid': {
                    'type': 'integer'
                },
                'description': {
                    'type': 'string',
                    'maxLength': 50
                }
            },
            'required': ['codelinkname','accountid','description']
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


class CodelinkSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'codelinkname': {
                    'type': 'string',
                    'maxLength': 20
                },
                'accountid': {
                    'type': 'integer'
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
