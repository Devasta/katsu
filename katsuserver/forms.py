import wtforms
import flask_wtf
import wtforms.fields.html5


class LoginForm(flask_wtf.FlaskForm):
    email = wtforms.fields.html5.EmailField('email',
                                            validators=[wtforms.validators.InputRequired(),
                                                        wtforms.validators.Email('Invalid Email')
                                                        ])
    password = wtforms.PasswordField('password',
                                     validators=[wtforms.validators.InputRequired()])
