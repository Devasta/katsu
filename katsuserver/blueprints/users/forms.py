import wtforms
import flask_wtf
from wtforms.fields.html5 import EmailField


class UserSearchForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    userid = wtforms.IntegerField('userid',
                                         validators=[wtforms.validators.Optional()
                                                     ])
    memberid = wtforms.IntegerField('memberid',
                                         validators=[wtforms.validators.Optional()
                                                     ])
    email = EmailField('email',
                                         validators=[wtforms.validators.Optional()
                                                     ])


