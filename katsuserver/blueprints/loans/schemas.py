import jsonschema


class LoanSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'memberid': {
                    'type': 'string',
                    'pattern': r'''[0-9]'''
                },
                'loanid': {
                    'type': 'string',
                    'pattern': r'''[0-9]'''
                },
                'status': {
                    'type': 'string',
                    'maxLength': 1
                },
                'paymentmethod': {
                    'type': 'string',
                    "enum": ['DD', 'CA']
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


class LoanSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'memberid': {
                    'type': 'integer'
                },
                'amount': {
                    'type': 'number',
                    'multipleOf': 0.01,  # 2 decimal places precision
                    'minimum': 0
                },
                'currency': {
                    'type': 'string',
                    'minimum': 3,
                    'maximum': 3
                },
                'purpose': {
                    'type': 'string',
                    'maxLength': 100
                },
                'status': {
                    'type': 'string',
                    'maxLength': 1
                },
                'interestrate': {
                    'type': 'number',
                    'multipleOf': 0.01,  # 2 decimal places precision
                    'minimum': 0
                },
                'paymentmethodid': {
                    'type': 'string',
                    "enum": ['DD', 'CA']
                },
                'paymentamount': {
                    'type': 'number',
                    'multipleOf': 0.01,  # 2 decimal places precision
                    'minimum': 0
                },
                'nextpaymentdate': {
                    'type': 'string',
                    'format': 'date'
                },
                'paymentfrequency': {
                    'type': 'string',
                    "enum": ['M', 'W', 'Q', 'F']
                },
                'closecode': {
                    'type': 'integer'
                },
                'savingsaccountid': {
                    'type': 'integer'
                }
            }
        }
        self.data = data
        self.errors = []

    def validate(self, method='NEW'):
        """
            We use the RFC-7396 JSON Merge Patch for the API, which may not necessarily receive all fields.
            We want to validate any fields we can, but must have additional checks for the mandatory fields, to ensure
            that there  are no attempts to delete them.

            It might be easier to have separate form classes for both methods. Feel free to change.
        """

        self.errors = []
        v = jsonschema.Draft202012Validator(self.schema)

        if v.is_valid(self.data):
            if method == 'NEW':
                if self.data.get('memberid') is None:
                    self.errors.append({'memberid': 'memberid cannot be null or empty.'})
                if self.data.get('amount') is None:
                    self.errors.append({'amount': 'loan amount cannot be null or empty.'})
                if self.data.get('currency') is None:
                    self.errors.append({'currency': 'loan amount cannot be null or empty.'})
                if self.data.get('purpose') is None:
                    self.errors.append({'amount': 'loan purpose cannot be null or empty.'})
                if self.data.get('statusid') is not None and self.data.get('statusid') != 'P':
                    self.errors.append({'statusid': "loan statusid must be set to 'P' for new loans. It will be automatically filled."})
            else:

                if 'memberid' in self.data and self.data.get('memberid') is None:
                    self.errors.append({'memberid': "memberid cannot be null or empty. Don't send if not changing."})
                if 'amount' in self.data and self.data.get('amount') is None:
                    self.errors.append({'amount': "amount cannot be null or empty. Don't send if not changing."})
                if 'currency' in self.data:
                    self.errors.append({'currency': "Currency cannot be changed."})
                if 'purpose' in self.data and self.data.get('purpose') is None:
                    self.errors.append({'purpose': "loan purpose cannot be null or empty. Don't send if not changing."})
                if 'statusid' in self.data and self.data.get('statusid') is None:
                    self.errors.append({'statusid': "loan statusid cannot be null or empty. Don't send if not changing."})
                if 'statusid' in self.data and self.data.get('statusid') == 'C' and 'closecode' not in self.data:
                    self.errors.append({'statusid':"cannot close loan without a reason provided."})
                if 'statusid' in self.data and self.data.get('statusid') != 'C' and 'closecode' in self.data:
                    self.errors.append({'statusid':"close reason provided but loan not closing."})
        else:
            self.errors = [error.message for error in sorted(v.iter_errors(self.data), key=str)]

        if len(self.errors) > 0:
            return False
        else:
            return True
