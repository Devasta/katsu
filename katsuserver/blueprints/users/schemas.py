import jsonschema

class usersearchschema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                    'userid': {
                        'type': 'integer'
                    },
                    'memberid': {
                        'type': 'integer'
                    },
                    'email': {
                        'type': 'string',
                        'format': 'email'
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
