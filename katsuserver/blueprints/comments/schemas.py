import jsonschema


class CommentSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'accountid': {
                    'type': 'integer'
                },
                'commenttext': {
                    'type': 'string',
                    'minLength': 1,
                    'maxLength': 200
                }
            },
            'required': ['accountid', 'commenttext']
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


class CommentSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'accountid': {
                    'type': 'integer'
                },
                'memberid': {
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