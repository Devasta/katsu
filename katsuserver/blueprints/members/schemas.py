import jsonschema


class membersearchschema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'memberid': {
                    'type': 'integer'
                },
                'surname': {
                    'type': 'string',
                    'maxLength': 35
                },
                'addressline1': {
                    'type': 'string',
                    'maxLength': 50
                },
                'county': {
                    'type': 'string',
                    'maxLength': 50
                },
                'postcode': {
                    'type': 'string',
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
            self.errors = [error.message for error in sorted(v.iter_errors(self.data), key=str)]
            return False



class memberdetailsschema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'title': {
                    'type': 'string',
                    "enum": ['Mr', 'Mrs', 'Miss', 'Ms', 'Dr', 'Prof']
                },
                'forename': {
                    'type': 'string',
                    'maxLength': 35
                },
                'surname': {
                    'type': 'string',
                    'maxLength': 35
                },
                'companyname': {
                    'type': 'string',
                    'maxLength': 100
                },
                'addressline1': {
                    'type': 'string',
                    'minLength': 1,
                    'maxLength': 50
                },
                'addressline2': {
                    'type': 'string',
                    'maxLength': 50
                },
                'city': {
                    'type': 'string',
                    'maxLength': 50
                },
                'county': {
                    'type': 'string',
                    'maxLength': 50
                },
                'country': {
                    'type': 'string',
                    'maxLength': 50
                },
                'postcode': {
                    'type': 'string',
                    'pattern': '^[A-Za-z0-9]{3}[ ]{1}[A-Za-z0-9]{4}$'
                },
                'homephone': {
                    'type': 'string',
                    'maxLength': 20
                },
                'mobilephone': {
                    'type': 'string',
                    'maxLength': 20
                },
                'dateofbiorth': {
                    'type': 'string',
                    'format': 'date'
                }
            },
            'required': ['addressline1','county','postcode']
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



