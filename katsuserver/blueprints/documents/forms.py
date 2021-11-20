import flask_wtf
import wtforms


class documentuploadform(flask_wtf.FlaskForm):
    accountid = wtforms.IntegerField('accountid',
                                   validators=[wtforms.validators.InputRequired()
                                               ])
    document = wtforms.FileField('document',
                                 validators=[wtforms.validators.InputRequired()
                                             ])
    description = wtforms.StringField('description',
                                 validators=[wtforms.validators.InputRequired()
                                             ])
    # TODO Should I only allow certain file extensions be loaded?


class documentsearchform(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    accountid = wtforms.IntegerField('accountid',
                                     validators=[wtforms.validators.Optional()
                                                 ]
                                     )
    memberid = wtforms.IntegerField('memberid',
                                    validators=[wtforms.validators.Optional()
                                                ]
                                    )
