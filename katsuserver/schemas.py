import jsonschema


class LoginSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'email': {
                    # https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression
                    'type': 'string',
                    'pattern': r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''',
                    "format": "email",
                },
                'password': {
                    'type': 'string'
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
