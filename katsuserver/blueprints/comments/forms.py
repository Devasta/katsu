import wtforms
import flask_wtf


class CommentSearchForm(flask_wtf.FlaskForm):
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


class commententryform(flask_wtf.FlaskForm):
    accountid = wtforms.IntegerField('accountid',
                                   validators=[wtforms.validators.InputRequired()
                                               ])
    commenttext = wtforms.StringField('commenttext',
                                   widget=wtforms.widgets.TextArea(),
                                   validators=[wtforms.validators.InputRequired(),
                                               wtforms.validators.length(min=1, message='Please enter a comment.')
                                               ])




