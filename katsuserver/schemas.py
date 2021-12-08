import jsonschema


class LoginSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'email': {
                    'type': 'string',
                    "format": "email",
                    'required': True
                },
                'password': {
                    'type': 'string',
                    'required': True
                }
            },
            'required': ['email', 'password']
        }
        self.data = data
        self.errors = []

    def validate(self):
        self.errors = []
        v = jsonschema.Draft202012Validator(self.schema)
        if v.is_valid(self.data):
            return True
        else:
            #print(v.iter_errors(self.data))
            #print(v.iter_errors())
            self.errors = [error.message for error in v.iter_errors(self.data)]
            return False
