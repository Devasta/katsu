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
