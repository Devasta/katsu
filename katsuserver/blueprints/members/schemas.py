import jsonschema


class membersearchschema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'memberid': {
                    'type': 'integer',
                    'required': False
                },
                'surname': {
                    'type': 'string',
                    'required': False,
                    'maxLength': 35
                },
                'addressline1': {
                    'type': 'string',
                    'required': False,
                    'maxLength': 50
                },
                'county': {
                    'type': 'string',
                    'required': False,
                    'maxLength': 50
                },
                'postcode': {
                    'type': 'string',
                    'required': False,
                    'pattern': '^[A-Za-z0-9]{3}[ ]{1}[A-Za-z0-9]{4}$'
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
