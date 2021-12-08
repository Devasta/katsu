import jsonschema

class usersearchschema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                    'userid': {
                        'type': 'integer',
                        'required': False
                    },
                    'memberid': {
                        'type': 'integer',
                        'required': False
                    },
                    'email': {
                        'type': 'string',
                        'format': 'email',
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
