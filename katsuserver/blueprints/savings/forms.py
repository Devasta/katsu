import flask_wtf
import wtforms


class SavingsSearchForm(flask_wtf.FlaskForm):
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
    status = wtforms.StringField('status',
                                 validators=[wtforms.validators.Optional(),
                                             wtforms.validators.Length(max=1)
                                             ]
                                 )


class SavingsAccountForm(flask_wtf.FlaskForm):
    memberid = wtforms.IntegerField('memberid',
                                   validators=[wtforms.validators.InputRequired()
                                               ])
