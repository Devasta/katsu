import jsonschema
from jsonschema import SchemaError

'''
class ConfigsForm(flask_wtf.FlaskForm):
    configname = wtforms.StringField('configname',
                                        validators=[wtforms.validators.InputRequired(),
                                                    wtforms.validators.Length(max=20)
                                                    ])
    configvalue = wtforms.StringField('configvalue',
                                        validators=[wtforms.validators.InputRequired(),
                                                    wtforms.validators.Length(max=50)
                                                    ])
    description = wtforms.StringField('description',
                                        validators=[wtforms.validators.InputRequired(),
                                                    wtforms.validators.Length(max=50)
                                                    ])
'''


class ConfigSchema:

    def __init__(self, data):
        self.schema = {
            'type': 'object',
            'properties': {
                'configname': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 20
                },
                'configvalue': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 50
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
