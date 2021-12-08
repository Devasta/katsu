import jsonschema

"""
    http://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields

    We will always be loading a transaction with multiple child records, so need to validate all at once.

    REST be damned, if we were really concerned with REST we wouldn't be using JSON.
"""

class TransactionSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'accountid': {
                    'type': 'integer',
                    'required': False
                },
                'transactionid': {
                    'type': 'integer',
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


class BasicTransactionSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'accountid': {
                    'type': 'integer',
                    'required': True
                },
                'description': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 200
                },
                'amount': {
                    'type': 'number',
                    'multipleOf': 0.01,  # 2 decimal places precision
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


class DetailedTransactionSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'description': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 200
                },
            'entries': {
                'type': 'array',
                'items': [
                            {
                            'type':'object',
                            'properties': {
                                'accountid': {
                                    'type': 'integer',
                                    'required': True
                                },
                                'debit': {
                                    'type': 'string',
                                    'required': True,
                                    'enum': ['Debit', 'Credit']
                                },
                                'amount': {
                                    'type': 'number',
                                    'multipleOf': 0.01,  # 2 decimal places precision
                                    'minimum': 0,
                                    'required': True
                                }
                            }
                        }
                    ]
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


