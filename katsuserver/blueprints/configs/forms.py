import wtforms
import flask_wtf


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


class ConfigSearchForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    configname = wtforms.StringField('configname',
                                        validators=[wtforms.validators.Optional(),
                                                    wtforms.validators.Length(max=20)
                                                    ])
