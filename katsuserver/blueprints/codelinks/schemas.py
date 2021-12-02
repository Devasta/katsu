import jsonschema

'''
import wtforms
import flask_wtf


class CodelinksForm(flask_wtf.FlaskForm):
    codelinkname = wtforms.StringField('codelinkname',
                                        validators=[wtforms.validators.InputRequired(),
                                                    wtforms.validators.Length(max=20)
                                                    ])
    accountid = wtforms.IntegerField('accountid',
                                        validators=[wtforms.validators.InputRequired(),
                                                    ])
    description = wtforms.StringField('description',
                                        validators=[wtforms.validators.InputRequired(),
                                                    wtforms.validators.Length(max=50)
                                                    ])


class CodelinkSearchForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    codelinkname = wtforms.StringField('codelinkname',
                                        validators=[wtforms.validators.Optional(),
                                                    wtforms.validators.Length(max=20)
                                                    ])
    accountid = wtforms.IntegerField('accountid',
                                        validators=[wtforms.validators.Optional(),
                                                    ])

'''

class CodelinkSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'codelinkname': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 20
                },
                'accountid': {
                    'type': 'integer',
                    'required': True
                },
                'description': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 50
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


class CodelinkSearchSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'codelinkname': {
                    'type': 'string',
                    'required': False,
                    'maxLength': 20
                },
                'accountid': {
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
