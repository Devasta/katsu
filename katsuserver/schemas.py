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
