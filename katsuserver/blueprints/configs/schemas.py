import jsonschema


class ConfigSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'configname': {
                    'type': 'string',
                    'maxLength': 20
                },
                'configvalue': {
                    'type': 'string',
                    'maxLength': 50
                },
                'description': {
                    'type': 'string',
                    'maxLength': 50
                }
            },
            'required': ['configname', 'configvalue', 'description']
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


class ConfigSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'configname': {
                    'type': 'string',
                    'maxLength': 20
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
